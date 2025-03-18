"""app_main views"""

import json
import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
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
        # result = csi.get_result()
        result = {"success": True, "name": "jaroslav-curda"}
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
        context["name"] = self.kwargs.get("name")
        return context


class ComparePinView(View):
    """Porovnej pin s databazi"""

    def post(self, request, *args, **kwargs):
        """ziskej data z formulare"""
        form_name = request.POST.get("name")
        form_pin = request.POST.get("pin")
        print(form_name)

        employee_name = Employee.objects.filter(slug="jaroslav-curda").first()
        if employee_name:
            print(employee_name.check_pin_code(form_pin))
        else:
            cons.log("jmeno nenalezeno", style="red")

        messages.error(request, "nespravny PIN")
        return redirect("mainpage", 15)
