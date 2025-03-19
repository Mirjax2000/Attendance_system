"""dashboard views CBVs"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
    View,
)
from rich.console import Console

from app_main.models import Department, Employee, EmployeeStatus

# importuju instanci tridy Camsystems
from attendance.cam_systems import cam_systems_instance as csi
from attendance.settings import DEBUG

from .forms import EmployeeForm

cons: Console = Console()
# instance CamSystems


def get_user(view_instance) -> dict:
    """Získej jméno přihlášeného uživatele"""
    status: str = ""
    current_user = view_instance.request.user
    name: str = str(current_user.username)

    if current_user.is_superuser:
        status = "SuperUser"
    elif current_user.is_staff:
        status = "admin"

    return {"username": name, "status": status}


class RedirectDashboard(RedirectView):
    """Redirect na /dashboard/main_panel"""

    url = "dashboard/main_panel"


class MainPanelView(LoginRequiredMixin, ListView):
    """homepage"""

    template_name = "app_dashboard/main_panel.html"
    model = Department
    context_object_name = "departments"

    def get_queryset(self):
        # Získání querysetu a přidání počtu zaměstnanců pomocí annotate
        queryset = Department.objects.annotate(employee_count=Count("employee"))
        return queryset

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "main-panel"

        return context


class EmployeesView(LoginRequiredMixin, ListView):
    """Seznam vsech zamestnancu"""

    model = Employee
    template_name = "app_dashboard/employees.html"
    context_object_name = "employees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "employees"

        return context


class VacationView(LoginRequiredMixin, ListView):
    """Seznam vsech zamestnancu"""

    model = Employee
    template_name = "app_dashboard/vacation.html"
    context_object_name = "vacations"

    def get_queryset(self):
        queryset = Employee.objects.filter(employee_status__name="vacation")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "vacations"

        return context


class WorkingView(LoginRequiredMixin, ListView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/working.html"
    model = Employee
    context_object_name = "working_employees"

    def get_queryset(self):
        queryset = Employee.objects.filter(employee_status__name="working")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "works"

        return context


class SickView(LoginRequiredMixin, ListView):
    """Seznam vsech zamestnancu"""

    model = Employee
    context_object_name = "sick_employees"
    template_name = "app_dashboard/sick.html"

    def get_queryset(self):
        queryset = Employee.objects.filter(employee_status__name="sick_leave")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "sick"

        return context


class OtherView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/other.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "others"

        return context


class EmailView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/emails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "emails"

        return context


class ChartsView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "charts"

        return context


class AttendanceView(LoginRequiredMixin, TemplateView):
    """detail o zamestanci"""

    template_name = "app_dashboard/attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "attendances"

        return context


class CamView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        context["user_name"] = get_user(self)
        context["active_link"] = "cams"
        return context


class CreateEmpView(CreateView):
    """Vytvor zamestance"""

    model = Employee
    form_class = EmployeeForm
    template_name = "includes/create_emp_form.html"
    success_url = reverse_lazy("employees")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Zaměstnanec byl úspěšně vytvořen!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Chyba - záznam nebyl vytvořen")
        return response


class DepartmentListView(ListView):
    """Vypis users"""

    model = Department
    template_name = "app_dashboard/department_list.html"
    context_object_name = "departments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "main-panel"

        return context


class TakeVectorView(LoginRequiredMixin, DetailView):
    """Take vector from camera"""

    model = Employee
    template_name = "app_dashboard/take_vector.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "employees"

        return context


class SaveVectorToDbView(LoginRequiredMixin, View):
    """Volání z employee detail.html z tlacitka
    take vector
    """

    def get(self, request, *args, **kwargs):
        """Získá slug zaměstnance z URL a uloží vektor do databáze."""
        employee_slug = self.kwargs.get("slug")

        if not employee_slug:
            messages.error(request, "Chybí jmeno zaměstnance!")
            return redirect("employees")

        result = csi.database.save_vector_to_db(employee_slug)
        if DEBUG:
            cons.log(result["message"], style="green")

        if result["success"]:
            messages.success(request, result["message"])
            return redirect("employees")

        messages.error(request, result["message"])
        return redirect("employees")


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    """User Delete"""

    model = Employee
    template_name = "app_dashboard/delete_employee.html"
    success_url = reverse_lazy("employees")

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")  # Získání slugu z URL
        return get_object_or_404(Employee, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "employees"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.get_object()} smazan")
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    """Update user"""

    model = Employee
    form_class = EmployeeForm
    template_name = "includes/create_emp_form.html"
    success_url = reverse_lazy("employees")

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")  # Získání slugu z URL
        return get_object_or_404(Employee, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "employees"

        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.get_object()}: Updated")
        return super().form_valid(form)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    """Detail user"""

    model = Employee
    template_name = "app_dashboard/employee_detail.html"
    context_object_name = "employee"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")  # Získání slugu z URL
        return get_object_or_404(Employee, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user(self)
        context["active_link"] = "employees"

        return context


class StatusView(TemplateView):
    """
    stav databaze, ruzne vypisy do contextu
    """

    template_name = "app_dashboard/status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        statuses = [
            "working",
            "sick_leave",
            "business_trip",
            "vacation",
            "free",
        ]

        existing_statuses = [
            status.name
            for status in EmployeeStatus.objects.filter(name__in=statuses)
        ]

        missing_statuses = set(statuses) - set(existing_statuses)

        context["existing_statuses"] = existing_statuses
        context["missing_statuses"] = missing_statuses
        context["department_nezarazeno"] = Department.objects.filter(
            name="nezarazeno"
        ).exists()
        context["active_link"] = "status"
        return context


class DepartmentDetailList(LoginRequiredMixin, ListView):
    """seznam zamestnacu z FK department"""

    template_name = "app_dashboard/department_detail_list.html"
    model = Employee
    context_object_name = "employees"

    def get_queryset(self):
        department_id = self.kwargs.get("pk")
        return Employee.objects.filter(department_id=department_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_id = self.kwargs.get("pk")
        department = get_object_or_404(Department, pk=department_id)
        context["department"] = department
        context["user_name"] = get_user(self)
        context["active_link"] = "main-panel"

        return context
