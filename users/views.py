from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"


class UserTasks(LoginRequiredMixin, ListView):
    template_name = "users/task_list.html"

    def get_queryset(self):
        return self.request.user.tasks.all()


class Profile(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    model = User
    template_name = "users/profile.html"
