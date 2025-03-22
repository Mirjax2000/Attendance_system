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

    def clean_email(self) -> str:
        """Kontrola emailu a převod na lowercase"""
        email: str = self.cleaned_data.get("email").lower()
        existing_emails = Employee.objects.filter(email__iexact=email)
        if self.instance.pk:
            existing_emails = existing_emails.exclude(pk=self.instance.pk)
        if existing_emails.exists():
            raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
        return email

    def clean_postal_code(self) -> str:
        """Kontrola formátu a délky psč, odstranění mezer"""
        postal_code: str = self.cleaned_data.get('postal_code', '').strip()
        postal_code_no_spaces = postal_code.replace(' ', '')
        if (len(postal_code_no_spaces
                ) != 5 or not postal_code_no_spaces.isdigit()):
            raise ValidationError(
                "PSČ musí obsahovat přesně 5 číslic bez mezer.")
        return postal_code_no_spaces

    def clean_phone_number(self) -> str:
        """Kontrola formátu tel. čísla"""
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

    def clean_pin_code(self) -> str:
        """Kontrola formátu pin kódu"""
        pin_code: str = self.cleaned_data.get('pin_code')
        if not pin_code.isdigit() or len(pin_code) != 4:
            raise ValidationError("PIN kód musí obsahovat přesně 4 číslice.")
        return pin_code

    def clean_date_of_birth(self) -> date:
        """Kontrola data narození (nesmí být v budoucnu)"""
        date_of_birth: date = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise ValidationError("Datum narození je povinné.")
        if date_of_birth > date.today():
            raise ValidationError("Datum narození nemůže být v budoucnosti.")
        return date_of_birth

    def clean_name(self) -> str:
        """Kontrola jména (velké písmeno a znaky)"""
        name: str = self.cleaned_data.get('name').strip().capitalize()
        if not name.isalpha():
            raise ValidationError("Jméno smí obsahovat pouze znaky abecedy.")
        return name

    def clean_surname(self) -> str:
        """Kontrola příjmení (velké písmeno a znaky)"""
        surname: str = self.cleaned_data.get('surname').strip().capitalize()
        if not surname.isalpha():
            raise ValidationError(
                "Příjmení smí obsahovat pouze znaky abecedy.")
        return surname
