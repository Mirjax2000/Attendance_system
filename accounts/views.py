"""Account views"""

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from accounts.forms import SignUpForm, UserUpdateForm


def get_user_name(view_instance) -> str:
    """Získej jméno přihlášeného uživatele"""
    result: str = str(view_instance.request.user.username)
    return result


class UserListView(LoginRequiredMixin, ListView):
    """Vypis users"""

    model = User
    template_name = "accounts/user_list_detail.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    """Detail user"""

    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "user"

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
    success_url = reverse_lazy("user_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.get_object()}: Updated")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """User Delete"""

    model = User
    template_name = "registration/delete_user.html"
    success_url = reverse_lazy("user_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"
        return context

    def control(self):
        """Self protection"""
        current_user = get_user_name(self)
        user_to_delete = str(self.get_object())
        if current_user == user_to_delete:
            messages.error(self.request, "Nemuzes smazat sam sebe")
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self.control():
            return redirect("user_list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f"{self.get_object()} smazan")
        return super().form_valid(form)


class SignUpView(CreateView):
    """User create"""

    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("user_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = get_user_name(self)
        context["active_link"] = "main-panel"

        return context

    def form_valid(self, form):
        user = form.save()  # Uloží nového uživatele
        user_name = user.username
        messages.success(self.request, f"Uživatel {user_name} vytvořen")
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
            return redirect("main_panel")
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        form.add_error(None, "Nepodařilo se přihlásit, zkuste to znovu.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Přihlášení bylo úspěšné!")
        return super().form_valid(form)
