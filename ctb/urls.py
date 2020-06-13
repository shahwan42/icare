"""ctb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home') Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include

from pages.views import Home
from core.views import NewTask, TaskUpdatedWebhook
from users.views import UserTasks, Profile, ChangePassword

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("task_updated", TaskUpdatedWebhook.as_view(), name="task_updated"),
    # path("new_task_space/<int:space_id>", NewTaskInSpace.as_view(), name="new_task_space"),
    path("new_task/<int:folder_id>", NewTask.as_view(), name="new_task"),
    path(
        "new_task/success",
        TemplateView.as_view(template_name="core/new_task_success.html"),
        name="new_task_success",
    ),
    # path("users/", include("users.urls")),
    path("users/tasks", UserTasks.as_view(), name="user_tasks"),
    path("users/profile/<int:pk>", Profile.as_view(), name="user_profile"),
    path("users/password_change/", ChangePassword.as_view(), name="password_change"),
    path("users/", include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "CTB Admin"
admin.site.site_title = "CTB Admin Portal"
admin.site.index_title = "Welcome to CTB Portal"
admin.site.unregister(Group)
