"""app_main views"""

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .cam_systems import CamSystems

# instance CamSystems
cam_system = CamSystems()


class MainPageView(TemplateView):
    """main page view"""

    template_name = "app_main/app_main.html"


class CamStreamView(View):
    """video streaming"""

    def get(self, request, *args, **kwargs):
        """get the fps value"""
        speed = kwargs.get("speed", 15)  # Získání hodnoty z URL

        return cam_system.cam_stream(speed)
