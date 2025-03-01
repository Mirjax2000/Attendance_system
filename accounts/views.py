from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages



def user_logout(request):
    """Logout a redirect"""
    logout(request)
    return redirect('dashboard')


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request,
                       "Nepodařilo se přihlásit, zkuste to znovu.")

        return redirect('dashboard')

