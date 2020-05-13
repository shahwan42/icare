from django.views.generic import ListView

from core.models import CSpace


class Home(ListView):
    template_name = "pages/home.html"
    queryset = CSpace.objects.filter(is_active=True)
