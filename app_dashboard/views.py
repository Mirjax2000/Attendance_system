from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)


class MainPanelView(LoginRequiredMixin, TemplateView):
    """homepage"""

    template_name = "app_main/main_panel.html"


class AllEmployeesView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/employees.html"


class VacationView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/vacation.html"


class WorkingView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/working.html"


class SickView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/sick.html"


class OtherView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/other.html"


class EmailView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_main/emails.html"


class ChartsView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_main/charts.html"


class CamView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        return context
