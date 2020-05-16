from django.views.generic import ListView

from core.models import Space, Folder


class HomeWithSpaces(ListView):
    """DEPRECATED
    List active spaces to put tasks in"""

    template_name = "pages/home.html"
    queryset = Space.objects.filter(is_active=True)


class Home(ListView):
    """List active folders to put tasks in"""

    template_name = "pages/home.html"
    queryset = Folder.objects.filter(is_active=True)
