from django.contrib import admin

from .models import CTeam, CSpace, CFolder, CList, CTask, Webhook


class CListInlineAdmin(admin.TabularInline):
    model = CList


class CTeamAdmin(admin.ModelAdmin):
    list_display = ["c_id", "name", "is_active"]


class CSpaceAdmin(admin.ModelAdmin):
    list_display = ["c_id", "name", "is_active"]


class CFolderAdmin(admin.ModelAdmin):
    inlines = (CListInlineAdmin,)
    list_display = ["c_id", "name", "is_active"]


class CListAdmin(admin.ModelAdmin):
    list_display = ["c_id", "name", "is_active"]


class CTaskAdmin(admin.ModelAdmin):
    list_display = ["c_id", "name", "is_active"]


class WebhookAdmin(admin.ModelAdmin):
    list_display = ["c_id", "c_team"]


admin.site.register(CTeam, CTeamAdmin)
# admin.site.register(CSpace, CSpaceAdmin)
admin.site.register(CFolder, CFolderAdmin)
admin.site.register(CList, CListAdmin)
admin.site.register(CTask, CTaskAdmin)
# admin.site.register(Webhook, WebhookAdmin)
