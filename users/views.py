from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"


class UserTasks(LoginRequiredMixin, ListView):
    template_name = "users/task_list.html"

    def get_queryset(self):
        return self.request.user.tasks.all()
