from django.views.generic import ListView

from core.models import CSpace, CFolder


class HomeWithSpaces(ListView):
    """DEPRECATED
    List active spaces to put tasks in"""

    template_name = "pages/home.html"
    queryset = CSpace.objects.filter(is_active=True)


class Home(ListView):
    """List active folders to put tasks in"""

    template_name = "pages/home.html"
    queryset = CFolder.objects.filter(is_active=True)
