"""app_main views"""

import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    View,
)
from rich.console import Console

# importuju instanci tridy Camsystems
from cam_systems import cam_systems_instance as csi

from .models import Employee

cons: Console = Console()


class MainPageView(LoginRequiredMixin, TemplateView):
    """main page view"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speed"] = self.kwargs.get("speed", 15)
        return context

    template_name = "app_main/app_main.html"


class CamStreamView(LoginRequiredMixin, View):
    """video streaming"""

    def get(self, request, *args, **kwargs):
        """get the fps value"""
        speed = kwargs.get("speed", 15)  # Získání hodnoty z URL

        return csi.cam_stream(speed)


class GetResultView(LoginRequiredMixin, View):
    """Volání funkce get result z cam_system.py"""

    def post(self, request, *args, **kwargs):
        """ziska vysledek z funkce get_result
        vraci message : name nebo popis chyby
        vraci success True or false
        """
        result = csi.get_result()
        # result = {"success": True, "name": "jaroslav-curda"}
        cons.log(result)

        if result["success"]:
            # predani jmena do API
            return redirect("check_pin", result["name"])

        messages.error(request, result["message"])
        return redirect("mainpage", 15)


class CheckPinView(TemplateView):
    """stranka na kotrolu Pinu"""

    template_name = "app_main/check-pin.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["name"] = self.kwargs.get("slug")
        return context


class ComparePinView(View):
    """Porovnej pin s databazi"""

    def post(self, request, *args, **kwargs):
        """ziskej data z formulare"""
        form_name = request.POST.get("name", None)
        form_pin = request.POST.get("pin", None)
        if not form_name or not form_pin:
            # Pokud není 'name' nebo 'pin' v POST, můžeš reagovat
            messages.error(request, "Musíte zadat jméno a PIN.")
            return redirect("mainpage", 15)

        # instance zamestnance
        try:
            employee = Employee.objects.get(slug=form_name)
            cons.log(f"jmeno nalezeno:{employee.slug}", style="blue")

            # kontrola pinhash vs form pin
            if employee.check_pin_code(form_pin):
                messages.success(
                    request, f"zamestnanec potvrzen: {employee.slug}"
                )
                return redirect("emp_login", employee.slug)

            messages.error(request, "nespravny PIN")
            return redirect("mainpage", 15)

        except Employee.DoesNotExist:
            # velmi vzacne / prakticky nemozne
            messages.error(request, "zamestnanec neni v databazi")
            return redirect("mainpage", 15)


class EmpLoginView(TemplateView):
    """stranka se zadavanim stavu v Employee status"""

    template_name = "app_main/emp_login.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["name"] = self.kwargs.get("slug")
        return context


class SetStatusView(View):
    """nastav databazi"""

    def post(self, request, *args, **kwargs):
        """prijme data z formulare
        jmeno a Workstatus
        nastavy pozadovany stav v DB
        """
        emp_status = request.POST.get("statusVal", None)
        emp_name = request.POST.get("name", None)
        print(emp_name, emp_status)
        time.sleep(5)
        return redirect("mainpage", 15)
