"""Forms"""

from django import forms

from app_main import models


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
            },
        }
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "pin_code": forms.PasswordInput(attrs={"maxlength": 4}),
        }
