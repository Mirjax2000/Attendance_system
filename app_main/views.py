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

# Create your views here.


class MainPageView(TemplateView):
    """main page view"""

    template_name = "app_main/app_main.html"
