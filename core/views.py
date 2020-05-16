import json

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

from .models import CSpace, CFolder, CList, CTask
from . import utils as u, payloads as p
from .forms import NewTaskForm


class NewTaskInSpace(View):
    """DEPRECATED
    Create a new task within a Space"""

    form_class = NewTaskForm
    template_name = "core/new_task.html"

    def get(self, request, *args, **kwargs):
        space_id = kwargs.get("space_id")
        qs = CSpace.objects.filter(c_id=space_id, is_active=True)
        if not qs.exists():
            raise Http404

        lists = list()
        space = qs.first()
        for folder in space.folders.filter(is_active=True):
            for clist in folder.lists.filter(is_active=True):
                lists.append(clist)

        form = NewTaskForm([(c_list.c_id, c_list.name) for c_list in lists])

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise HttpResponseNotAllowed

        name = request.POST.get("name")
        description = request.POST.get("description")
        c_list_id = request.POST.get("c_list")

        # create new task on clickup
        remote_task = u.create_task(c_list_id, p.create_task_payload(name, description))

        qs = CList.objects.filter(c_id=str(c_list_id), is_active=True)
        if not qs.exists():
            raise Http404
        c_list = qs.first()

        # save task representation locally after making sure it's created
        if remote_task:
            CTask.objects.create(
                c_id=remote_task.get("id"),
                c_json_res=remote_task,
                name=remote_task.get("name"),
                description=remote_task.get("description"),
                c_list=c_list,
                is_active=True,
                user=request.user,
                status=remote_task.get("status").get("status"),
            )

        return redirect(reverse("new_task_success"))


def get_folder_from_kwargs(kwargs):
    folder_id = kwargs.get("folder_id")
    qs = CFolder.objects.filter(c_id=folder_id, is_active=True)
    if not qs.exists():
        raise Http404
    folder = qs.first()
    return folder


class NewTask(View):
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
            c_list = cd.get("c_list")
        else:
            return HttpResponseBadRequest("Invalid data")

        # create new task on clickup
        remote_task = u.create_task(
            c_list.c_id, p.create_task_payload(name, description)
        )

        # save task representation locally after making sure it's created
        if remote_task:
            CTask.objects.create(
                c_id=remote_task.get("id"),
                c_json_res=remote_task,
                name=remote_task.get("name"),
                description=remote_task.get("description"),
                c_list=c_list,
                is_active=True,
                user=request.user,
                status=remote_task.get("status").get("status"),
            )

        return redirect(reverse("new_task_success"))


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
            qs = CTask.objects.filter(c_id=remote_task.get("task_id"))
            if qs.exists():
                task = qs.first()
                task.c_update_json_res = remote_task
                task.status = (
                    remote_task.get("history_items")[0].get("after").get("status")
                )
                task.save()
        return JsonResponse({}, status=200)
