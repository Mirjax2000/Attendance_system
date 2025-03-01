from django.contrib.auth import logout
from django.shortcuts import redirect


def user_logout(request):
    """Logout a redirect"""
    logout(request)
    return redirect("dashboard")
