from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class NewRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    due_date = serializers.DateField(required=False)
    list_id = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        list_id = attrs.get("list_id")

        try:
            ls = List.objects.get(id=list_id)
        except List.DoesNotExist:
            raise ValidationError({"list_id": "Not found"})

        if not ls.is_active:
            raise ValidationError({"list_id": "Inactive list"})

        attrs["list"] = ls

        return attrs


class UpdateRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    due_date = serializers.DateField(required=False)
    request_id = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        request_id = attrs.get("request_id")

        try:
            req = Task.objects.get(id=request_id)
        except Task.DoesNotExist:
            raise ValidationError({"request_id": "Not found"})

        if not req.is_active:
            raise ValidationError({"request_id": "Inactive Request"})

        attrs["task"] = req

        return attrs
