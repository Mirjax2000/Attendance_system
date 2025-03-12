"""Acounts formulare"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import (
    CharField,
    DateField,
    EmailField,
    ModelForm,
    NumberInput,
    PasswordInput,
    Textarea,
    ValidationError,
)

User = get_user_model()


class SignUpForm(UserCreationForm):
    """Formular pro noveho uzivatele"""

    username = CharField(
        max_length=20, label="Uživatelské jméno", required=True
    )
    first_name = CharField(max_length=30, label="Jméno", required=True)
    last_name = CharField(max_length=30, label="Příjmení", required=True)
    password1 = CharField(widget=PasswordInput(), label="Heslo")
    password2 = CharField(
        widget=PasswordInput(),
        label="Heslo znovu",
    )
    email = EmailField(max_length=50, label="E-mail", required=True)

    class Meta(UserCreationForm.Meta):
        """Meta pole"""

        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_email(self):
        """Kontrola emailu"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
        return email


class UserUpdateForm(ModelForm):
    """Formulář pro aktualizaci uživatele (bez hesla)"""

    username = CharField(max_length=20, label="Uživatelské jméno")

    first_name = CharField(max_length=30, label="Jméno")
    last_name = CharField(max_length=30, label="Příjmení")
    email = EmailField(max_length=50, label="E-mail")

    class Meta:
        """zobrazeni poli"""

        model = User
        fields = ["username", "first_name", "last_name", "email"]
