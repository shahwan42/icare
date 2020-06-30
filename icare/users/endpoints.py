from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated

from icare.core.models import Task
from icare.core.serializers import TaskSerializer
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import CustomUser as User


class Requests(ListAPIView):
    """List user's requests"""

    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class Profile(APIView):
    """Retrieve/Update/partial update user's data(profile)"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"name": request.user.name, "email": request.user.email})

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        return Response({"name": updated_user.name, "email": updated_user.email})

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        return Response({"name": updated_user.name, "email": updated_user.email})


class Password(UpdateAPIView):
    """Change user's password"""

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password
        if not self.object.check_password(serializer.data.get("old_password")):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # set_password also hashes the password that the user will get
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()

        return Response({"message": "Password updated successfully"})


class Register(CreateAPIView):
    """Register a new user"""

    serializer_class = UserSerializer
    model = User


class Logout(APIView):
    """Logout a user (remove his/her token)"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        return Response()
