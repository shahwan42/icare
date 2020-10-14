from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework.authtoken import views


from icare.pages.views import Home
from icare.core.views import NewTask, TaskUpdatedWebhook, ListCustomFields
from icare.users.views import UserTasks, Profile, ChangePassword

# API imports
from icare.users.endpoints import (
    Profile as ProfileApi,
    Requests,
    Password,
    Register,
    Logout,
)
from icare.core.endpoints import (
    Folders,
    FolderDetail,
    ICareRequest,
    RequestAttachment,
)  # ,Lists


api_urls = [
    # Users API
    path("api/user/token", views.obtain_auth_token, name="user_token"),
    path("api/user/logout", Logout.as_view(), name="user_logout"),
    path("api/user/register", Register.as_view(), name="user_register"),
    path("api/user/profile", ProfileApi.as_view(), name="user_profile"),
    path("api/user/password", Password.as_view(), name="user_password"),
    path("api/user/requests", Requests.as_view(), name="user_requests"),
    # Folders API
    path("api/folders", Folders.as_view(), name="core_folders"),
    path("api/folders/<int:pk>", FolderDetail.as_view(), name="core_folder"),
    # Lists API  NOTE: not needed for now, folder details shows related lists
    # path("api/lists", Lists.as_view(), name="core_lists"),
    # Requests (Tasks) API
    path("api/icare_request", ICareRequest.as_view(), name="icare_request"),
    path("api/attachment", RequestAttachment.as_view(), name="attachment"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("task_updated", TaskUpdatedWebhook.as_view(), name="task_updated"),
    path("new_task/<int:folder_id>", NewTask.as_view(), name="new_task"),
    path(
        "lists/<int:pk>/custom_fields",
        ListCustomFields.as_view(),
        name="list_custom_fields",
    ),
    path(
        "new_task/success",
        TemplateView.as_view(template_name="core/new_task_success.html"),
        name="new_task_success",
    ),
    path("users/", include("icare.users.urls")),
    path("users/tasks", UserTasks.as_view(), name="user_tasks"),
    path("users/profile/<int:pk>", Profile.as_view(), name="user_profile"),
    path("users/password_change/", ChangePassword.as_view(), name="password_change"),
    path("users/", include("django.contrib.auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
] + api_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "I Care Administration"
admin.site.site_title = "Administration"
admin.site.index_title = "Welcome"
admin.site.unregister(Group)
