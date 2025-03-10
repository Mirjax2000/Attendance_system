from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


def user_logout(request):
    """Logout a redirect"""
    logout(request)
    return redirect("dashboard")


class CustomLoginView(LoginView):
    """login form"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        form.add_error(None, "Nepodařilo se přihlásit, zkuste to znovu.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Přihlášení bylo úspěšné!")
        return super().form_valid(form)
