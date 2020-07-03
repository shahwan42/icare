from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from .models import (
    Team,
    Folder,
    List,
    Task,
    ListCustomField,
    TaskCustomField,
)  # , Webhook  # , Space
from . import utils as u


# ============================= Inlines
class ListInline(admin.TabularInline):
    model = List
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 36})},
    }
    readonly_fields = ("clickup_id", "name", "description")


class TaskInline(admin.TabularInline):
    model = Task
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "20"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 36})},
    }
    fields = ("is_active", "clickup_id", "name", "description")
    readonly_fields = (
        "clickup_id",
        "name",
        "description",
        "user",
    )


class ListCustomFieldInline(admin.TabularInline):
    model = List.custom_fields.through


class TaskCustomFieldInline(admin.TabularInline):
    model = TaskCustomField


# ============================= Actions
def import_data(modeladmin, request, queryset):
    for obj in queryset:
        print("==========================================")
        print("Importing form inside admin panel...")
        print("==========================================")
        team_name = u.import_teams_data(obj.clickup_id)
        print("==========================================")
        print("Done importing from inside admin panel...")
        print("==========================================")
        obj.is_imported = True
        obj.name = team_name
        obj.save()


import_data.short_description = "Import team's data"


def import_custom_fields(modeladmin, request, queryset):
    print("==========================================")
    print("Importing List Custom Fields form inside admin panel...")
    print("==========================================")
    for obj in queryset:
        print(f"Importing Custom Fields for <List {obj.clickup_id}>")
        custom_fields = u.get_custom_fields(obj.clickup_id)
        if len(custom_fields) > 0:
            for field in custom_fields:
                lcf, created = ListCustomField.objects.get_or_create(
                    clickup_id=field.get("id"), _type=field.get("type")
                )
                if created:
                    lcf.name = field.get("name")
                    lcf.created_json = field
                    if field.get("type") == "drop_down":
                        lcf.type_config = field.get("type_config")
                lcf.lists.add(obj)
                lcf.save()

            obj.custom_fields_imported = True
            obj.save()
    print("==========================================")
    print("Done importing List Custom Fields from inside admin panel...")
    print("==========================================")


import_custom_fields.short_description = "Import custom fields"


def activate(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_active = True
        obj.save()


# ============================= Admins
class TeamAdmin(admin.ModelAdmin):
    list_display = ["clickup_id", "name", "is_active"]
    actions = [import_data]


class SpaceAdmin(admin.ModelAdmin):
    list_display = ["clickup_id", "name", "is_active"]
    readonly_fields = ("clickup_id", "name", "description", "team")


class FolderAdmin(admin.ModelAdmin):
    inlines = (ListInline,)
    list_display = ["clickup_id", "name", "is_active"]
    readonly_fields = ("clickup_id", "name", "description", "space")
    actions = [activate]


class ListAdmin(admin.ModelAdmin):
    inlines = (TaskInline, ListCustomFieldInline)
    list_display = ["clickup_id", "name", "is_active"]
    readonly_fields = (
        "clickup_id",
        "name",
        "description",
        "folder",
        "custom_fields_imported",
    )
    actions = [import_custom_fields, activate]


class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskCustomFieldInline,)
    list_display = [
        "clickup_id",
        "name",
        "is_active",
        "list_clickup_id",
        "list_name",
        "user_name",
        "user_email",
    ]
    readonly_fields = (
        "clickup_id",
        "name",
        "description",
        "created_json",
        "updated_json",
        "_list",
        "user",
    )


class ListCustomFieldAdmin(admin.ModelAdmin):
    readonly_fields = (
        "clickup_id",
        "name",
        "created_json",
        "lists",
        "_type",
        "type_config",
    )


class WebhookAdmin(admin.ModelAdmin):
    list_display = ["clickup_id", "team"]
    readonly_fields = ("clickup_id", "team", "created_json")


admin.site.register(Team, TeamAdmin)
# admin.site.register(Space, SpaceAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Task, TaskAdmin)
# admin.site.register(Webhook, WebhookAdmin)
admin.site.register(ListCustomField, ListCustomFieldAdmin)
