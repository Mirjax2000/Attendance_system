from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    """Home page"""
    return render(request=request, template_name="app_main/home.html")


def custom_404(request, exception):
    """Chybova stranka jen kdyz DEBUG=False"""
    html = render_to_string("404.html", {"message": str(exception)})
    return HttpResponseNotFound(html)


def cam(request, speed: int = 10):
    """camera endpoint"""
    return render(request, "app_main/cam.html", {"speed": speed})
