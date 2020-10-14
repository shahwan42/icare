from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "name", "is_active", "is_superuser")
    list_editable = ("is_active", "is_superuser")
    list_display_links = ("email", "name")
    list_filter = ("is_superuser", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "phone_number", "avatar",)}),
        ("Permissions", {"fields": ("is_active", "is_superuser",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email", "name")


admin.site.register(CustomUser, CustomUserAdmin)
