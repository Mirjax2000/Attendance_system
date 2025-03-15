"""dashboard views CBVs"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
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
    View,
)
from rich.console import Console

from app_main.models import Department, Employee, FaceVector

# importuju instanci tridy Camsystems
from cam_systems import cam_systems_instance as csi

from .forms import EmployeeForm

cons: Console = Console()
# instance CamSystems


def get_user_name(view_instance) -> str:
    """Získej jméno přihlášeného uživatele"""
    result: str = str(view_instance.request.user.username)
    return result


class RedirectDashboard(RedirectView):
    """Redirect na /dashboard"""

    url = "dashboard"


class DashboardView(LoginRequiredMixin, TemplateView):
    """Homepage"""

    template_name = "app_dashboard/main_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context


class MainPanelView(LoginRequiredMixin, TemplateView):
    """homepage"""

    template_name = "app_dashboard/main_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context


class EmployeesView(LoginRequiredMixin, ListView):
    """Seznam vsech zamestnancu"""

    model = Employee
    template_name = "app_dashboard/employees.html"
    context_object_name = "employees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "employees"

        return context


class VacationView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/vacation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "vacations"

        return context


class WorkingView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/working.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "works"

        return context


class SickView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/sick.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "sick"

        return context


class OtherView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/other.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "others"

        return context


class EmailView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/emails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "emails"

        return context


class ChartsView(LoginRequiredMixin, TemplateView):
    """rozesilani emialu"""

    template_name = "app_dashboard/charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "charts"

        return context


class AttendanceView(LoginRequiredMixin, TemplateView):
    """detail o zamestanci"""

    template_name = "app_dashboard/attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "attendances"

        return context


class CamView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        context["user_name"] = get_user_name(self)
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


class DepartmentListView(ListView):
    """Vypis users"""

    model = Department
    template_name = "app_dashboard/department_list.html"
    context_object_name = "departments"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context


class TakeVectorView(LoginRequiredMixin, DetailView):
    """Take vector from camera"""

    model = Employee
    template_name = "app_dashboard/take_vector.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "employees"

        return context


# class SaveVectorToDbView(LoginRequiredMixin, View):
#     """Volání funkce z cam_system.py"""

#     def post(self, request, *args, **kwargs):
#         """post metoda"""
#         employee_slug = self.kwargs.get("slug", None)

#         return JsonResponse(csi.database.save_vector_to_db(employee_slug))

#     def get(self, request, *args, **kwargs):
#         """to je kdyby nebylo post"""
#         return JsonResponse(
#             {"message": "Špatná metoda u get_result"}, status=400
#         )


class SaveVectorToDbView(LoginRequiredMixin, View):
    """Volání z formuláře"""

    def post(self, request, *args, **kwargs):
        """post metoda"""
        employee_slug = self.kwargs.get("slug")

        if not employee_slug:
            messages.error(request, "Chybí slug zaměstnance!")
            return redirect("employees")

        result = csi.database.save_vector_to_db(employee_slug)
        cons.log(result, style="green")

        messages.success(request, "Vektor úspěšně uložen!")
        return redirect("employees")


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    """User Delete"""

    model = Employee
    template_name = "app_dashboard/delete_employee.html"
    success_url = reverse_lazy("employees")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "employees"

        return context
