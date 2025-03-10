"""dashboard views CBVs"""

from django.contrib import messages
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
from rich.console import Console

from app_main.models import Employee

from .forms import EmployeeForm

cons: Console = Console()


class RedirectDashboard(RedirectView):
    """Redirect na /dashboard"""

    url = "dashboard"


def get_user_name(view_instance) -> str:
    """Získej jméno přihlášeného uživatele"""
    result: str = str(view_instance.request.user.username)
    cons.log(f"Aktivni User: {result},", style="green")
    return result


class DashboardView(LoginRequiredMixin, TemplateView):
    """Homepage"""

    template_name = "app_dashboard/app_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class MainPanelView(LoginRequiredMixin, TemplateView):
    """homepage"""

    template_name = "app_dashboard/main_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class EmployeesView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/employees.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class VacationView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/vacation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class WorkingView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/working.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class SickView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/sick.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class OtherView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/other.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class EmailView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/emails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class ChartsView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class AttendanceView(LoginRequiredMixin, TemplateView):
    """detail o zamestanci"""

    template_name = "app_dashboard/attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)

        return context


class CamView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        context["user_name"] = get_user_name(self)
        return context


class CreateEmpView(CreateView):
    """Vytvor zamestance"""

    model = Employee
    form_class = EmployeeForm
    template_name = "includes/create_emp_form.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Zaměstnanec byl úspěšně vytvořen!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Chyba - záznam nebyl vytvořen")
        return response
