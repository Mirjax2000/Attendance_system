"""Acounts formulare"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import (
    ModelForm,
    ValidationError,
)

User = get_user_model()


class SignUpForm(UserCreationForm):
    """Formulář pro nového uživatele"""

    is_staff = forms.BooleanField(
        required=False,
        label="Je administrátor",
    )

    is_superuser = forms.BooleanField(
        required=False,
        label="Je superuživatel",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_staff",
            "is_superuser",
        ]
        labels = {
            "username": "Uživatelské jméno",
            "email": "E-mail",
            "first_name": "Jméno",
            "last_name": "Příjmení",
            "password1": "Heslo",
            "password2": "Heslo znovu",
        }

    def clean_email(self):
        """Kontrola emailu"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
        return email


class UserUpdateForm(ModelForm):
    """Formulář pro aktualizaci uživatele (bez hesla)"""

    class Meta:
        """zobrazeni poli"""

        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "username": "Uživatelské jméno",
            "first_name": "Jméno",
            "last_name": "Příjmení",
            "email": "E-mail",
        }

    # kdyz ji zapnes tak neulozis , proste neulozis, ne, nejde to
    # def clean_email(self):
    #     """Kontrola emailu"""
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(email__iexact=email).exists():
    #         raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
    #     return email
