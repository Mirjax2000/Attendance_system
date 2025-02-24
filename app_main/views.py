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
    """Homepage"""

    vystupDB = 0
    user_name = "Vigo"

    template_name = "app_main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.vystupDB == 1:
            context["user_exist"] = "True"
            context["user_name"] = self.user_name
        else:
            context["user_exist"] = "False"
            context["user_name"] = "Neprihlasen"

        return context


class MainPanelView(TemplateView):
    """homepage"""

    template_name = "app_main/main_panel.html"


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


class EmailView(TemplateView):
    """rozesilani emialu"""

    template_name = "app_main/emails.html"


class CamView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        return context
