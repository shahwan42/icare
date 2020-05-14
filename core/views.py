from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.http.response import HttpResponse, Http404, HttpResponseNotAllowed

from .models import CSpace, CList, CTask
from . import utils as u, payloads as p
from .forms import NewTaskForm


class NewTask(View):
    form_class = NewTaskForm
    template_name = "core/new_task.html"

    def get(self, request, *args, **kwargs):
        space_id = kwargs.get("space_id")
        qs = CSpace.objects.filter(c_id=space_id)
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
                status=remote_task.get("status"),
            )

        return redirect(reverse("new_task_success"))
