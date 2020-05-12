from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="Name:",
        widget=forms.TextInput(attrs={"class": "form-control", "size": 35}),
    )

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
