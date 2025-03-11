"""Acounts formulare"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import (
    CharField,
    DateField,
    EmailField,
    NumberInput,
    PasswordInput,
    Textarea,
    ValidationError,
)

User = get_user_model()


class SignUpForm(UserCreationForm):
    """Formular pro noveho uzivatele"""

    class Meta(UserCreationForm.Meta):
        """Meta pole"""

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Uživatelské jméno",
            "first_name": "Jméno",
            "last_name": "Příjmení",
        }

    password1 = CharField(widget=PasswordInput(), label="Heslo")

    password2 = CharField(
        widget=PasswordInput(),
        label="Heslo znovu",
    )
    email = EmailField(label="E-mail", required=True)

    def clean_email(self):
        """Kontrola emailu"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
        return email
