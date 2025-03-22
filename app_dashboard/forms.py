"""Forms"""
import re
from datetime import date

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

    def clean_email(self) -> str or None:
        """Kontrola emailu a převod na lowercase"""
        if self.cleaned_data.get("email") is not None:
            email: str = self.cleaned_data.get("email").lower()
            existing_emails = Employee.objects.filter(email__iexact=email)
            if self.instance.pk:
                existing_emails = existing_emails.exclude(pk=self.instance.pk)
            if existing_emails.exists():
                raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
            return email
        return None

    def clean_postal_code(self) -> str or None:
        """Kontrola formátu a délky psč, odstranění mezer"""
        if self.cleaned_data.get("postal_code") is not None:
            postal_code: str = self.cleaned_data.get('postal_code', '').strip()
            postal_code_no_spaces = postal_code.replace(' ', '')
            if (len(postal_code_no_spaces
                    ) != 5 or not postal_code_no_spaces.isdigit()):
                raise ValidationError(
                    "PSČ musí obsahovat přesně 5 číslic bez mezer.")
            return postal_code_no_spaces
        return None

    def clean_phone_number(self) -> str or None:
        """Kontrola formátu tel. čísla"""
        if self.cleaned_data.get("phone_number") is not None:
            phone_number: str = self.cleaned_data.get('phone_number')
            pattern: str = r'^\+420\s?(\d{3}\s?\d{3}\s?\d{3})$|^\d{9}$'
            if not phone_number:
                raise ValidationError("Telefonní číslo je povinné.")
            if not re.match(pattern, phone_number):
                raise ValidationError(
                    "Telefonní číslo musí být ve formátu +420 XXX XXX XXX nebo "
                    "9 číslic bez mezer."
                )
            return phone_number
        return None

    def clean_pin_code(self) -> str or None:
        """Kontrola formátu pin kódu"""
        if self.cleaned_data.get("pin_code") is not None:
            pin_code: str = self.cleaned_data.get('pin_code')
            if not pin_code.isdigit() or len(pin_code) != 4:
                raise ValidationError("PIN kód musí obsahovat přesně 4 číslice.")
            return pin_code
        return None

    def clean_date_of_birth(self) -> date or None:
        """Kontrola data narození (nesmí být v budoucnu)"""
        if self.cleaned_data.get("date_of_birth") is not None:
            date_of_birth: date = self.cleaned_data.get('date_of_birth')
            if not date_of_birth:
                raise ValidationError("Datum narození je povinné.")
            if date_of_birth > date.today():
                raise ValidationError("Datum narození nemůže být v budoucnosti.")
            return date_of_birth
        return None

    def clean_name(self) -> str or None:
        """Kontrola jména (velké písmeno a znaky)"""
        if self.cleaned_data.get('name') is not None:
            name: str = self.cleaned_data.get('name').strip().capitalize()
            if not name.isalpha():
                raise ValidationError("Jméno smí obsahovat pouze znaky abecedy.")
            return name
        return None

    def clean_surname(self) -> str or None:
        """Kontrola příjmení (velké písmeno a znaky)"""
        if self.cleaned_data.get('surname') is not None:
            surname: str = self.cleaned_data.get('surname').strip().capitalize()
            if not surname.isalpha():
                raise ValidationError(
                    "Příjmení smí obsahovat pouze znaky abecedy.")
            return surname
        return None
