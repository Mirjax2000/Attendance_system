"""Account views"""

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import SignUpForm, UserUpdateForm


def get_user_name(view_instance) -> str:
    """Získej jméno přihlášeného uživatele"""
    result: str = str(view_instance.request.user.username)
    return result


class UserListView(ListView):
    """Vypis users"""

    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update user"""

    model = User
    form_class = UserUpdateForm
    template_name = "registration/user_update.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Updated")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """User Delete"""

    model = User
    template_name = "registration/user_confirm_delete.html"
    success_url = reverse_lazy("dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Uživatel byl úspěšně smazán.")
        return super().delete(request, *args, **kwargs)


class SignUpView(CreateView):
    """User create"""

    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context

    def form_valid(self, form):
        messages.success(self.request, "Uživatel vytvořen")
        return super().form_valid(form)


def user_logout(request):
    """Logout a zustan na strance"""
    name = request.user.username
    logout(request)
    messages.success(request, f"Uživatel {name} odhlášen")
    return redirect(request.META.get("HTTP_REFERER", "/"))


# class CustomLogoutView(LogoutView):
#     """Logout view with message"""

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             messages.success(
#                 request, f"Uživatel {get_user_name(self)} odhlášen"
#             )
#         return super().dispatch(request, *args, **kwargs)

#     def get_next_page(self):
#         """Správné přesměrování po odhlášení"""
#         return self.request.META.get("HTTP_REFERER") or "/"


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
