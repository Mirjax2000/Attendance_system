"""dashboard views CBVs"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from app_main.models import Employee

from .forms import EmployeeForm


class RedirectDashboard(RedirectView):
    """Redirect na /dashboard"""

    url = "dashboard"


class DashboardView(TemplateView):
    """Homepage"""

    template_name = "app_dashboard/app_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_exist"] = "True"
            context["user_name"] = self.request.user.username
        else:
            context["user_exist"] = "False"
            context["user_name"] = "Nepřihlášen"
        return context


class MainPanelView(LoginRequiredMixin, TemplateView):
    """homepage"""

    template_name = "app_dashboard/main_panel.html"


class EmployeesView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/employees.html"


class VacationView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/vacation.html"


class WorkingView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/working.html"


class SickView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/sick.html"


class OtherView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/other.html"


class EmailView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/emails.html"


class ChartsView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/charts.html"


class AttendanceView(LoginRequiredMixin, TemplateView):
    """detail o zamestanci"""

    template_name = "app_dashboard/attendance.html"


class CamView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        return context


class CreateEmpView(CreateView):
    """Vytvor zamestance"""

    model = Employee
    form_class = EmployeeForm
    template_name = "includes/create_emp_form.html"
    success_url = reverse_lazy("dashboard")
