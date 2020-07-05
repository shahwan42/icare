"""API Endpoints For Tasks, Lists, and Folders"""

import logging
import sys
import time
import datetime

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import utils as u, payloads as p
from .models import List, Folder, Task, Attachment
from .serializers import (
    ListSerializer,
    FolderSerializer,
    FolderDetailSerializer,
    NewRequestSerializer,
    AttachmentSerializer,
    UpdateRequestSerializer,
)

logger = logging.getLogger(__name__)


# TODO Remove this after making sure it's not needed
class Lists(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListSerializer
    queryset = List.objects.all()


class Folders(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()


class FolderDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FolderDetailSerializer
    queryset = Folder.objects.all()


class ICareRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """New Request"""

        # data validation
        serializer = NewRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # data extraction
        vd = serializer.validated_data
        name = vd.get("name")
        description = vd.get("description")
        due_date = vd.get("due_date")
        _list = vd.get("list")

        # logic

        clickup_description = f"{description}\n\n user's email: {request.user.email}\n"
        if due_date:
            date_to_time = time.mktime(
                datetime.datetime.strptime(str(due_date), "%Y-%m-%d").timetuple()
            )
            due_date = int(date_to_time * 1000)

        remote_task = u.create_task(
            _list.clickup_id,
            p.create_task_payload(name, clickup_description, due_date=due_date,),
        )

        if remote_task and remote_task.get("err"):
            logger.error(str(remote_task), exc_info=sys.exc_info())
            return Response(
                {"detail": "Request creation failed. Try again later"}, status=400
            )

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

        return Response({"detail": "Request created successfully!"})

    def put(self, request, *args, **kwargs):
        """Update Request"""

        # data validation
        serializer = UpdateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # data extraction
        vd = serializer.validated_data
        name = vd.get("name")
        description = vd.get("description")
        due_date = vd.get("due_date")
        task = vd.get("task")

        # logic
        clickup_description = f"{description}\n\n user's email: {request.user.email}\n"
        if due_date:
            date_to_time = time.mktime(
                datetime.datetime.strptime(str(due_date), "%Y-%m-%d").timetuple()
            )
            due_date = int(date_to_time * 1000)

        remote_task = u.update_task(
            task.clickup_id,
            p.create_task_payload(name, clickup_description, due_date=due_date,),
        )

        if remote_task and remote_task.get("err"):
            logger.error(str(remote_task), exc_info=sys.exc_info())
            return Response(
                {"detail": "Updating Request failed. Try again later"}, status=400
            )

        # update task locally
        task.name = name
        task.description = description
        task.updated_json = remote_task
        task.save()

        return Response({"detail": "Request updated successfully!"})


class RequestAttachment(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AttachmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vd = serializer.validated_data
        file = vd.get("attachment")
        task = vd.get("task")

        created_json = u.attachment(task.clickup_id, file)
        Attachment.objects.create(task=task, created_json=created_json)

        return Response(created_json)
