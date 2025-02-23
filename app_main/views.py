"""app_main views"""

from django.http import HttpResponseNotFound
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# Create your views here.


class HomeView(TemplateView):
    """homepage"""

    template_name = "app_main/home.html"


class AllEmployeesView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/employees.html"


class VacationView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/vacation.html"


class WorkingView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/working.html"


class SickView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/sick.html"


class OtherView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/other.html"


class CamView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        return context
