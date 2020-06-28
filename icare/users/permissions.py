from rest_framework.permissions import BasePermission


class IsSameUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.pk == view.kwargs.get("pk")
