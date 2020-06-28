from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .models import CustomUser as User
from .permissions import IsSameUser


class UserRU(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsSameUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
