from django.http import HttpResponseNotFound
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string


def index(request):
    """Home page"""
    return render(request=request, template_name="index.html")


def custom_404(request, exception):
    """Chybova stranka jen kdyz DEBUG=False"""
    html = render_to_string("404.html", {"message": str(exception)})
    return HttpResponseNotFound(html)
