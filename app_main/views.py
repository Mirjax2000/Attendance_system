"""app_main views"""

import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import (
    TemplateView,
    View,
)

# importuju instanci tridy Camsystems
from cam_systems import cam_systems_instance as csi


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
    """Volání z JS"""

    def post(self, request, *args, **kwargs):
        """post metoda"""
        data = json.loads(request.body)
        employee_name = data.get("employeeName")

        return JsonResponse(csi.get_result())

    def get(self, request, *args, **kwargs):
        """to je kdyby nebylo post"""
        return JsonResponse(
            {"message": "Špatná metoda u get_result"}, status=400
        )
