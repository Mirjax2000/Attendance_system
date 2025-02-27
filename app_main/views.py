"""app_main views"""

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

from app_main.forms import LoginForm

# Create your views here.


class LoginView(FormView):
    template_name = "app_main/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")  # Přesměrování po úspěšném přihlášení

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class HomeView(LoginRequiredMixin,TemplateView):
    """Homepage"""

    template_name = "app_main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_exist"] = "True"
            context["user_name"] = self.request.user.username
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


class ChartsView(TemplateView):
    """rozesilani emialu"""

    template_name = "app_main/charts.html"


class CamView(TemplateView):
    """Seznam vsech zamestnancu"""

    template_name = "app_main/cam.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 10)
        return context
