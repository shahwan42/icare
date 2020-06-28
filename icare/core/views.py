import json

import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http.response import (
    Http404,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
    JsonResponse,
)

from .models import Folder, List, Task
from . import utils as u, payloads as p
from .forms import NewTaskForm

logger = logging.getLogger(__name__)


def get_folder_from_kwargs(kwargs):
    folder_id = kwargs.get("folder_id")
    qs = Folder.objects.filter(clickup_id=folder_id, is_active=True)
    if not qs.exists():
        raise Http404
    return qs.first()


class NewTask(LoginRequiredMixin, View):
    """Create a new task within a folder"""

    form_class = NewTaskForm
    template_name = "core/new_task.html"

    def get(self, request, *args, **kwargs):
        folder = get_folder_from_kwargs(kwargs)
        form = NewTaskForm(folder=folder)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise HttpResponseNotAllowed

        folder = get_folder_from_kwargs(kwargs)
        form = NewTaskForm(request.POST, folder=folder)

        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get("name")
            description = cd.get("description")
            due_date = cd.get("due_date")
            _list = cd.get("_list")
        else:
            return HttpResponseBadRequest("Invalid data")

        clickup_description = f"{description}\n\n user's email: {request.user.email}\n"
        due_date = int(due_date.timestamp() * 1000) if due_date else None

        # create new task on clickup
        remote_task = u.create_task(
            _list.clickup_id,
            p.create_task_payload(name, clickup_description, due_date=due_date,),
        )

        # save task representation locally after making sure it's created
        if remote_task and remote_task.get("err"):
            logger.error(remote_task)
            return HttpResponseBadRequest("Invalid data")

        Task.objects.create(
            clickup_id=remote_task.get("id"),
            created_json=remote_task,
            name=remote_task.get("name"),
            description=description,
            _list=_list,
            is_active=True,
            user=request.user,
            status=remote_task.get("status").get("status"),
        )

        return redirect(reverse("new_task_success"))


class ListCustomFields(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ListCustomFields, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        """Return list of customfields to be filled after selecting
        a list from the dropdown menu"""

        try:
            ls = List.objects.get(pk=pk)
        except List.DoesNotExist:
            return JsonResponse({"message": "List not found"}, status=404)

        custom_fields = ls.custom_fields.all()
        if not custom_fields.exists():
            return JsonResponse(
                {"message": "No custom fields found for that list"}, status=404
            )

        # construct custom fields data
        fields = []
        for field in custom_fields:
            fields.append(
                {
                    "clickup_id": field.clickup_id,
                    "name": field.name,
                    "type": field._type,
                    "type_config": field.type_config,
                }
            )

        return JsonResponse({"message": "List of custom fields", "fields": fields})


# ==================== Webhooks


class TaskUpdatedWebhook(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdatedWebhook, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if hasattr(request, "body"):
            # print(request.body)
            remote_task = json.loads(request.body)
            if not remote_task.get("task_id"):
                return JsonResponse(status=400)

            print(remote_task)
            logger.info(remote_task)
            history_items = remote_task.get("history_items")

            qs = Task.objects.filter(clickup_id=remote_task.get("task_id"))
            if qs.exists():
                task = qs.first()
                task.updated_json = remote_task

                if len(history_items) > 0:
                    # update status
                    if history_items[0].get("field") == "status":
                        task.status = history_items[0].get("after").get("status")

                task.save()
        return JsonResponse({}, status=200)
