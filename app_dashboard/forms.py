"""Forms"""

import re
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from app_main import models
from app_main.models import Department, Employee


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
            "date_of_birth": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
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
                raise ValidationError("Tento e-mail je již používán. Zvolte jiný.")
            return email
        return ""

    def clean_postal_code(self) -> str:
        """Kontrola formátu a délky psč, odstranění mezer"""
        if self.cleaned_data.get("postal_code") is not None:
            postal_code: str = str(self.cleaned_data.get("postal_code", "")).strip()
            postal_code_no_spaces = postal_code.replace(" ", "")
            if len(postal_code_no_spaces) != 5 or not postal_code_no_spaces.isdigit():
                raise ValidationError("PSČ musí obsahovat přesně 5 číslic bez mezer.")
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
                raise ValidationError("Datum narození nemůže být v budoucnosti.")
            return date_of_birth
        return None

    def clean_name(self) -> str:
        """Kontrola jména (velké písmeno a znaky)"""
        if self.cleaned_data.get("name") is not None:
            name: str = str(self.cleaned_data.get("name")).strip().capitalize()
            if not name.isalpha():
                raise ValidationError("Jméno smí obsahovat pouze znaky abecedy.")
            return name
        return ""

    def clean_surname(self) -> str:
        """Kontrola příjmení (velké písmeno a znaky)"""
        if self.cleaned_data.get("surname") is not None:
            surname: str = str(self.cleaned_data.get("surname")).strip().capitalize()
            if not surname.isalpha():
                raise ValidationError("Příjmení smí obsahovat pouze znaky abecedy.")
            return surname
        return ""


class DepartmentForm(forms.ModelForm):
    """Formulář pro vytvoření Departments"""

    class Meta:
        """pole a widgety"""

        model = models.Department
        fields = ["name"]
        labels = {"name": "jméno oddělení"}
        error_messages = {
            "name": {
                "required": "Jméno je povinné!",
                "max_length": "Jméno je příliš dlouhé! (max. 50 znaků)",
                "unique": "Tento Department již existuje",
            },
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Zadejte jméno oddělení",
                }
            ),
        }


class SendMailForm(forms.Form):
    """Formulář pro odesílání e-mailů"""

    DELIVERY_METHODS = (
        ("manual", "Manuální zadání"),
        ("employee", "Výběr zaměstnanců"),
        ("department", "Výběr oddělení"),
    )
    subject = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter Subject ..."}),
    )
    message = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(
            attrs={"class": "L-emails__message", "placeholder": "Enter message ..."}
        ),
        required=False,
    )
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHODS)
    emails = forms.CharField(required=False, widget=forms.Textarea)
    employee_ids = forms.ModelMultipleChoiceField(
        required=False, queryset=Employee.objects.all()
    )
    department = forms.ModelChoiceField(
        required=False, queryset=Department.objects.all()
    )
    use_template = forms.BooleanField(required=False)
    selected_template = forms.CharField(required=False)

    def clean_emails(self):
        """
        Ověří a vyčistí seznam e-mailových adres zadaných
        jako řetězec oddělený čárkou.
        """

        emails_raw = self.cleaned_data.get("emails", "").strip()

        if not emails_raw:
            return emails_raw

        emails_list = [
            email.strip() for email in emails_raw.split(",") if email.strip()
        ]
        invalid_emails = []
        for email in emails_list:
            try:
                validate_email(email)
            except ValidationError:
                invalid_emails.append(email)

        if invalid_emails:
            raise ValidationError(
                f"Následující e-mailové adresy mají neplatný formát: "
                f"{', '.join(invalid_emails)}"
            )

        return ", ".join(emails_list)

    def clean(self):
        """
        Provádí dodatečné ověření na základě pole „delivery_method“
        a zajišťuje, že povinná pole jsou vyplněna v závislosti na zvoleném
        způsobu doručení.
        """
        cleaned_data = super().clean()
        use_template = cleaned_data.get("use_template")
        selected_template = cleaned_data.get("selected_template")
        subject = cleaned_data.get("subject") or ""
        message = cleaned_data.get("message") or ""

        if len(subject) > 255:
            self.add_error("subject", "Předmět překročil maximální délku 255 znaků.")

        if len(message) > 5000:
            self.add_error(
                "message", "Obsah zprávy překročil maximální délku 5000 znaků."
            )

        if not subject.strip():
            self.add_error("subject", "Předmět nemůže být prázdný.")

        if not message.strip():
            self.add_error("message", "Zpráva nemůže být prázdná.")

        if use_template:
            if not selected_template:
                raise ValidationError(
                    "Vybrali jste použití šablony, ale nezvolili jste žádnou šablonu."
                )
            # Pokud je použitá šablona, nepotřebujeme message formuláře
            cleaned_data["message"] = ""  # Zajistíme, že "message" není potřeba
        else:
            if not message.strip():
                self.add_error(
                    "message", "Toto pole je povinné, pokud nepoužíváte šablonu!"
                )

        method = cleaned_data.get("delivery_method")
        if method == "manual":
            if not cleaned_data.get("emails"):
                self.add_error("emails", "Zadejte prosím e-mailové adresy.")
        elif method == "employee":
            if not cleaned_data.get("employee_ids"):
                self.add_error(
                    "employee_ids", "Vyberte prosím alespoň jednoho zaměstnance."
                )
        elif method == "department":
            if not cleaned_data.get("department"):
                self.add_error("department", "Vyberte prosím oddělení.")
        return cleaned_data
