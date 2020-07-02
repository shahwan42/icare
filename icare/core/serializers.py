from rest_framework import serializers

from .models import Task, List, Folder


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"


class FolderDetailSerializer(FolderSerializer):
    lists = ListSerializer(many=True, read_only=True)
