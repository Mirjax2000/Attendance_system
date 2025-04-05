"""dashboard views CBVs"""
from pathlib import Path
from time import sleep

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
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
from attendance import settings

# importuju instanci tridy Camsystems
from attendance.cam_systems import cam_systems_instance as csi
from attendance.history_status_manager import HistoryStatusManager
from attendance.populate_db import db_control
from attendance.settings import DEBUG

from .forms import DepartmentForm, EmployeeForm, SendMailForm

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


class MainPanelView(LoginRequiredMixin, TemplateView):
    """homepage"""

    template_name = "app_dashboard/main_panel.html"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)
        context = super().get_context_data(**kwargs)
        departments = Department.objects.annotate(
            employee_count=Count("employee")
        )
        emp_statuses = EmployeeStatus.objects.annotate(
            employee_count=Count("employee")
        )

        context["departments"] = departments
        context["emp_statuses"] = emp_statuses
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "main-panel"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class EmployeesView(LoginRequiredMixin, ListView):
    """Seznam vsech zamestnancu"""

    model = Employee
    template_name = "app_dashboard/employees.html"
    context_object_name = "employees"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class CommonContextMixin:
    def get_context_data(self, **extra_context):
        user: dict = get_user(self)

        common_context = {
            "username": user["username"],
            "status": user["status"],
            "active_link": "send_mail_view",
            "db_good_condition": (
                    Department.objects.filter(name="nezarazeno").exists()
                    and EmployeeStatus.objects.values_list("name",
                                                           flat=True).distinct().count() >= 5
            ),
        }
        common_context.update(extra_context)
        return common_context


class SendMailView(LoginRequiredMixin, CommonContextMixin, View):
    """Odesílání mailů"""
    template_name_success = 'includes/success_mail.html'
    template_name_form = 'includes/mail_form.html'

    def get(self, request):
        form = SendMailForm()
        context = self.get_context_data(form=form)
        return render(request, self.template_name_form, context)

    def post(self, request):
        form = SendMailForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            delivery_method = form.cleaned_data['delivery_method']

            if form.cleaned_data.get('use_template'):
                selected_template = form.cleaned_data.get('selected_template')
                template_path = f'emails/{selected_template}.html'
                html_message = render_to_string(template_path)
            else:
                plain_message = form.cleaned_data['message']
                html_message = plain_message.replace('\n', '<br>')

            emails = []

            if delivery_method == 'manual':
                emails = [email.strip() for email in
                          form.cleaned_data['emails'].split(',')]
            elif delivery_method == 'employee':
                employees = form.cleaned_data['employee_ids']
                emails = [emp.email for emp in employees]
            elif delivery_method == 'department':
                department = form.cleaned_data['department']
                emails = [emp.email for emp in department.employee_set.all()]

            try:
                send_mail(
                    subject=subject,
                    message='Pro zobrazení emailu použijte klienta podporující HTML.',
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=emails,
                    fail_silently=False
                )
                context = self.get_context_data(
                    message='Email byl úspěšně odeslán!')
                return render(request, self.template_name_success, context)

            except Exception as e:
                form.add_error(None, f'Chyba při odesílání emailu: {str(e)}')

        context = self.get_context_data(form=form)
        return render(request, 'includes/mail_form_partial.html', context)


class MailManualPartialView(LoginRequiredMixin, View):
    """Partial pro manuální zadání mailových adres"""
    template_name = 'includes/message_manual.html'

    def get(self, request):
        form = SendMailForm()
        return render(request, self.template_name, {'form': form})


class MailEmployeePartialView(LoginRequiredMixin, View):
    """Partial pro výběr mailových adres zaměstnanců"""
    template_name = 'includes/mail_employee.html'

    def get(self, request):
        form = SendMailForm()
        return render(request, self.template_name, {'form': form})


class MailDepartmentPartialView(LoginRequiredMixin, View):
    """Partial pro výběr mailových adres celého oddělení"""
    template_name = 'includes/mail_department.html'

    def get(self, request):
        form = SendMailForm()
        return render(request, self.template_name, {'form': form})


class MailTemplatePartialView(View):
    """Partial pro aktualizaci výběru templates v mailovém klientu"""
    template_name = "includes/mail_template.html"

    def get_email_templates(self):
        template_dir = Path("app_dashboard/templates/emails/").resolve()
        templates = [f.stem for f in template_dir.glob("*.html") if
                     f.is_file()]
        return templates

    def get(self, request, *args, **kwargs):
        context = {
            "templates": self.get_email_templates()
        }
        return render(request, self.template_name, context)
    

class LoadMailTemplateContentView(View):
    """response pro AJAX volání k načtení HTML mailové templaty a doplnění do message"""
    def get(self, request, *args, **kwargs):
        template_name = request.GET.get("template_name")

        if not template_name:
            return JsonResponse({"error": "Chybí název šablony."}, status=400)

        full_template_name = f'emails/{template_name}.html'

        try:
            content = render_to_string(full_template_name,
                                       request=request)
            return JsonResponse({"content": content.strip()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)


class ChartsView(LoginRequiredMixin, TemplateView):
    """
    webové zobrazení pro vizualizaci.
    """
    template_name = "app_dashboard/charts.html"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "charts"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class AttendanceView(LoginRequiredMixin, TemplateView):
    """detail o zamestanci"""

    template_name = "app_dashboard/attendance.html"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)
        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "attendances"

        # Získání všech zaměstnanců
        employees = Employee.objects.all()

        # Pro každý zaměstnanec získat počet hodin, které odpracoval daný den
        employee_hours = []
        for employee in employees:
            zamestnanec = HistoryStatusManager(
                employee.slug
            )  # Vytvoření instance pro každého zaměstnanca
            worked_hours = zamestnanec.get_worked_hours_on_day("2025-03-24")
            employee_hours.append(
                {"employee": employee, "worked_hours": worked_hours}
            )

        context["employee_hours"] = employee_hours

        # Zkontrolování stavu databáze
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class CamView(LoginRequiredMixin, TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_dashboard/cam.html"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["speed"] = self.kwargs.get("speed", 10)
        context["active_link"] = "cams"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )
        return context


class CreateEmpView(CreateView):
    """Vytvor zamestance"""

    model = Employee
    form_class = EmployeeForm
    template_name = "includes/create_emp_form.html"
    success_url = reverse_lazy("employees")

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["user_name"] = get_user(self)
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )
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
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "main-panel"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class CreateDepView(CreateView):
    """Vytvor zamestance"""

    model = Department
    form_class = DepartmentForm
    template_name = "includes/create_dep_form.html"
    success_url = reverse_lazy("department_list")

    def get_initial(self):
        return {"name": ""}

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["user_name"] = get_user(self)
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Department byl úspěšně vytvořen!")
        return response


class TakeVectorView(LoginRequiredMixin, DetailView):
    """Take vector from camera"""

    model = Employee
    template_name = "app_dashboard/take_vector.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class DeleteDepView(LoginRequiredMixin, DeleteView):
    """Delete department"""

    model = Department
    template_name = "includes/delete_department.html"
    success_url = reverse_lazy("department_list")

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.get_object()} smazan")
        return super().form_valid(form)


class UpdateDepView(LoginRequiredMixin, UpdateView):
    """Update Department"""

    model = Department
    form_class = DepartmentForm
    template_name = "includes/create_dep_form.html"
    success_url = reverse_lazy("department_list")

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.get_object()}: Updated")
        return super().form_valid(form)


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
    template_name = "includes/delete_employee.html"
    success_url = reverse_lazy("employees")

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")  # Získání slugu z URL
        return get_object_or_404(Employee, slug=slug)

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )
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
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

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
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["active_link"] = "employees"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class StatusView(LoginRequiredMixin, TemplateView):
    """
    stav databaze, ruzne vypisy do contextu
    """

    template_name = "app_dashboard/status.html"

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]

        statuses = [
            "working",
            "sick_leave",
            "business_trip",
            "vacation",
            "free",
        ]

        existing_statuses: list = [
            status.name
            for status in EmployeeStatus.objects.filter(name__in=statuses)
        ]

        missing_statuses: set = set(statuses) - set(existing_statuses)

        context["existing_statuses"] = existing_statuses
        context["missing_statuses"] = missing_statuses
        context["department_nezarazeno"] = Department.objects.filter(
            name="nezarazeno"
        )
        context["active_link"] = "status"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )
        context["employee_count"] = Employee.objects.aggregate(
            total=Count("name")
        )["total"]

        return context


class FillDbView(LoginRequiredMixin, View):
    """spustit funkci na zaplneni databaze"""

    def get(self, request, *args, **kwargs):
        """spusti akci"""
        db_control.run_all_default()
        sleep(1)
        messages.success(request, "databáze zaplněna")
        return redirect("status")


class ResetDbView(LoginRequiredMixin, View):
    """spustit funkci na zaplneni databaze"""

    def get(self, request, *args, **kwargs):
        """spusti akci"""
        try:
            result = db_control.delete_db()
            if result:
                messages.success(request, "databáze vymazana")
            else:
                messages.error(request, "databáze nebyla vymazana")
        except Exception as e:
            messages.error(
                request, f"Došlo k chybě při vymazávání databáze: {str(e)}"
            )

        return redirect("status")


class DepartmentDetailList(LoginRequiredMixin, ListView):
    """seznam zamestnacu z FK department"""

    template_name = "app_dashboard/department_detail_list.html"
    model = Employee
    context_object_name = "employees"

    def get_queryset(self):
        department_id = self.kwargs.get("pk")
        return Employee.objects.filter(department_id=department_id)

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)
        department_id = self.kwargs.get("pk")
        department = get_object_or_404(Department, pk=department_id)

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["department"] = department
        context["active_link"] = "main-panel"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context


class EmpStatusDetailList(LoginRequiredMixin, ListView):
    """seznam zamestnacu z FK department"""

    template_name = "app_dashboard/status_detail_list.html"
    model = Employee
    context_object_name = "employees"

    def get_queryset(self):
        employee_status_id = self.kwargs.get("pk")
        return Employee.objects.filter(employee_status_id=employee_status_id)

    def get_context_data(self, **kwargs):
        user: dict = get_user(self)
        employee_status_id = self.kwargs.get("pk")
        employee_status = get_object_or_404(
            EmployeeStatus, pk=employee_status_id
        )

        context = super().get_context_data(**kwargs)
        context["username"] = user["username"]
        context["status"] = user["status"]
        context["emp_status"] = employee_status
        context["active_link"] = "main-panel"
        context["db_good_condition"] = (
            Department.objects.filter(name="nezarazeno").exists()
            and EmployeeStatus.objects.values_list("name", flat=True)
            .distinct()
            .count()
            >= 5
        )

        return context
