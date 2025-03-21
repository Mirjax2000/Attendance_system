"""Forms"""
import re

from django import forms
from django.core.exceptions import ValidationError

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

    def clean_email(self):
        """Kontrola emailu a převod na lowercase"""
        email = self.cleaned_data.get("email").lower()
        existing_emails = Employee.objects.filter(email__iexact=email)
        if self.instance.pk:
            existing_emails = existing_emails.exclude(pk=self.instance.pk)
        if existing_emails.exists():
            raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
        return email

    def clean_phone_number(self):
        """Kontrola formátu tel. čísla"""
        phone_number = self.cleaned_data.get('phone_number')
        pattern = r'^\+420\s?(\d{3}\s?\d{3}\s?\d{3})$|^\d{9}$'
        if not phone_number:
            raise ValidationError("Telefonní číslo je povinné.")
        if not re.match(pattern, phone_number):
            raise ValidationError(
                "Zadejte platné české telefonní číslo (+420 XXX XXX XXX nebo "
                "XXXXXXXXX).")
        return phone_number

    def clean_pin_code(self):
        """Kontrola formátu pin kódu"""
        pin_code = self.cleaned_data.get('pin_code')
        if not pin_code.isdigit() or len(pin_code) != 4:
            raise ValidationError("PIN kód musí obsahovat přesně 4 číslice.")
        return pin_code
