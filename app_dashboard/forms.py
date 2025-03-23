"""Forms"""

import re
from datetime import date
from typing import Any, Dict, List

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from app_main import models
from app_main.models import Employee


class EmployeeForm(forms.ModelForm):
    """Formulář pro vytvoření zaměstnance"""

    class Meta:
        """pole a widgety"""

        model = models.Employee
        fields = [
            "name",
            "surname",
            "street_number",
            "city",
            "postal_code",
            "phone_number",
            "email",
            "date_of_birth",
            "pin_code",
            "department",
            "employee_status",
        ]
        error_messages = {
            "name": {
                "required": "Jméno je povinné!",
                "max_length": "Jméno je příliš dlouhé! (max. 32 znaků)",
            },
            "surname": {
                "required": "Příjmení je povinné!",
            },
            "postal_code": {
                "invalid": "PSČ musí obsahovat 5 číslic.",
            },
            "phone_number": {
                "invalid": "Telefonní číslo musí být ve správném formátu.",
                "unique": "Tento telefon jiz existuje",
            },
            "email": {
                "unique": "Tento e-mail je již registrován!",
                "invalid": "Zadejte platnou e-mailovou adresu.",
            },
            "pin_code": {
                "invalid": "PIN musí obsahovat přesně 4 číslice.",
                "required": "Toto pole je povinné",
            },
        }
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "pin_code": forms.PasswordInput(attrs={"maxlength": 4}),
        }

    def clean_email(self) -> str:
        """Kontrola emailu a převod na lowercase"""
        if self.cleaned_data.get("email") is not None:
            email: str = str(self.cleaned_data.get("email")).lower()
            existing_emails = Employee.objects.filter(email__iexact=email)
            if self.instance.pk:
                existing_emails = existing_emails.exclude(pk=self.instance.pk)
            if existing_emails.exists():
                raise ValidationError(
                    "Tento e-mail je již používán. Zvolte jiný."
                )
            return email
        return ""

    def clean_postal_code(self) -> str:
        """Kontrola formátu a délky psč, odstranění mezer"""
        if self.cleaned_data.get("postal_code") is not None:
            postal_code: str = str(
                self.cleaned_data.get("postal_code", "")
            ).strip()
            postal_code_no_spaces = postal_code.replace(" ", "")
            if (
                len(postal_code_no_spaces) != 5
                or not postal_code_no_spaces.isdigit()
            ):
                raise ValidationError(
                    "PSČ musí obsahovat přesně 5 číslic bez mezer."
                )
            return postal_code_no_spaces
        return ""

    def clean_phone_number(self) -> str:
        """Kontrola formátu tel. čísla"""
        if self.cleaned_data.get("phone_number") is not None:
            phone_number: str = str(self.cleaned_data.get("phone_number"))
            pattern: str = r"^\+420\s?(\d{3}\s?\d{3}\s?\d{3})$|^\d{9}$"
            if not phone_number:
                raise ValidationError("Telefonní číslo je povinné.")
            if not re.match(pattern, phone_number):
                raise ValidationError(
                    "Telefonní číslo musí být ve formátu +420 XXX XXX XXX nebo "
                    "9 číslic bez mezer."
                )
            return phone_number
        return ""

    def clean_pin_code(self) -> str:
        """Kontrola formátu pin kódu"""
        if self.instance.pk:
            return self.cleaned_data.get("pin_code", "")
        if self.cleaned_data.get("pin_code") is not None:
            pin_code: str = str(self.cleaned_data.get("pin_code"))
            if not pin_code.isdigit() or len(pin_code) != 4:
                raise ValidationError("PIN musí obsahovat přesně 4 číslice.")
            return pin_code
        return ""

    def clean_date_of_birth(self) -> date | None:
        """Kontrola data narození (nesmí být v budoucnu)"""
        if self.cleaned_data.get("date_of_birth") is not None:
            date_of_birth = self.cleaned_data.get("date_of_birth")
            if not date_of_birth:
                raise ValidationError("Datum narození je povinné.")
            if date_of_birth > date.today():
                raise ValidationError(
                    "Datum narození nemůže být v budoucnosti."
                )
            return date_of_birth
        return None

    def clean_name(self) -> str:
        """Kontrola jména (velké písmeno a znaky)"""
        if self.cleaned_data.get("name") is not None:
            name: str = str(self.cleaned_data.get("name")).strip().capitalize()
            if not name.isalpha():
                raise ValidationError(
                    "Jméno smí obsahovat pouze znaky abecedy."
                )
            return name
        return ""

    def clean_surname(self) -> str:
        """Kontrola příjmení (velké písmeno a znaky)"""
        if self.cleaned_data.get("surname") is not None:
            surname: str = (
                str(self.cleaned_data.get("surname")).strip().capitalize()
            )
            if not surname.isalpha():
                raise ValidationError(
                    "Příjmení smí obsahovat pouze znaky abecedy."
                )
            return surname
        return ""


class EmailForm(forms.Form):
    """
    Třída řeší formulář pro odesílaní mailů
    """

    recipient_email = forms.CharField(label="Komu", required=True)
    subject = forms.CharField(label="Předmět", max_length=100, required=True)
    message = forms.CharField(
        label="Zpráva", widget=forms.Textarea, required=True
    )

    def clean_recipient_email(self) -> List[str]:
        """
        Validuje a čistí vstupy formuláře
        """
        value: str = self.cleaned_data["recipient_email"]
        # Rozdělení e-mailových adres oddělených čárkou
        email_list: List[str] = [
            email.strip() for email in value.split(",") if email.strip()
        ]
        if not email_list:
            raise forms.ValidationError(
                "Musíte zadat alespoň jednu platnou e-mailovou adresu."
            )

        email_validator = EmailValidator()
        banned_domains = ["spam.com", "neplatna-domena.cz"]
        valid_emails: List[str] = []

        for email in email_list:
            # Validace formátu e-mailové adresy
            try:
                email_validator(email)
            except forms.ValidationError:
                raise forms.ValidationError(
                    f"E-mailová adresa '{email}' má neplatný formát."
                )

            # Ověření nepovolených domén
            domain: str = email.split("@")[-1]
            if domain in banned_domains:
                raise forms.ValidationError(
                    f"E-mailová adresa '{email}' z této domény není povolena."
                )

            valid_emails.append(email)

        return valid_emails

    def clean(self) -> Dict[str, Any]:
        """
        Validuje a čistí vstupy formuláře
        """
        cleaned_data: Dict[str, Any] = super().clean()
        # Jelikož jsou pole povinná, očekáváme, že hodnoty existují
        subject: str = cleaned_data.get("subject", "")
        message: str = cleaned_data.get("message", "")

        if subject.lower() in message.lower():
            self.add_error("subject", "Předmět by neměl být obsažen ve zprávě.")

        if len(message.strip()) < 10:
            self.add_error(
                "message",
                "Zpráva je příliš krátká, musí obsahovat alespoň 10 znaků.",
            )

        return cleaned_data
