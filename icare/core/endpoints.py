"""API Endpoints For Tasks, Lists, and Folders"""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import List
from .serializers import ListSerializer


# TODO filter lists per folder
class Lists(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListSerializer
    queryset = List.objects.all()
