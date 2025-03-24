"""app-main Models"""

import os
from datetime import date, datetime, timedelta
from json import JSONDecodeError, dumps, loads

from cryptography.fernet import Fernet
from django.contrib.auth.hashers import check_password, make_password
from django.core import validators as val
from django.db import models
from django.db import transaction as tran
from django.forms import ValidationError
from django.utils.text import slugify
from django.utils.timezone import now
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
key: str = os.getenv("FERNET_KEY", default="")
fernet = Fernet(key)

con: Console = Console()


class Employee(models.Model):
    """Employee"""

    name = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Jméno:"
    )
    surname = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Příjmení:"
    )
    street_number = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="Ulice/č.p.:"
    )
    city = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Město:"
    )

    postal_code = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        verbose_name="PSČ:",
        validators=[
            val.MinLengthValidator(5),
            val.RegexValidator(
                regex=r"^\d{5}$", message="PSČ musí obsahovat 5 číslic."
            ),
        ],
    )

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Telefon:",
        validators=[
            val.MinLengthValidator(5),
            val.RegexValidator(
                regex=r"^\+?[0-9\s\-()]{5,13}$",
                message="Telefon musí být ve správném formátu.",
            ),
        ],
    )

    email = models.EmailField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Email:",
    )
    date_of_birth = models.DateField(
        null=False,
        blank=False,
        verbose_name="Datum narození:",
    )
    is_valid = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Ucet v poradku?:",
    )
    pin_code = models.CharField(
        max_length=4,
        blank=True,
        null=False,
        verbose_name="PIN kod:",
        validators=[
            val.RegexValidator(
                regex=r"^\d{4}$",
                message="PIN musí obsahovat přesně 4 číslice.",
                code="invalid_pin",
            )
        ],
    )
    pin_code_hash = models.CharField(
        max_length=255, blank=True, null=False, verbose_name="Pin Hash:"
    )

    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Oddělení",
    )

    employee_status = models.ForeignKey(
        "EmployeeStatus",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="pracovni status",
    )

    slug = models.SlugField(
        blank=True,
        unique=True,
        verbose_name="slug:",
    )

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    def __repr__(self) -> str:
        return f"Employee: {self.name} {self.surname} {self.status()}"

    def set_slug(self) -> None:
        """Vytvor slug"""
        self.slug = slugify(f"{self.name}-{self.surname}")

    def status(self) -> str:
        """Status"""
        if self.is_valid:
            return "is valid"
        return "is invalid"

    def date_of_birth_format(self) -> str:
        """Datum narozeni formatovani"""
        if self.date_of_birth:
            return self.date_of_birth.strftime("%Y-%m-%d")
        return "N/A"

    def age(self) -> int:
        """Vypocet veku"""
        if self.date_of_birth:
            today = date.today()
            age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
            return age
        return 0

    def set_pin_hash(self) -> None:
        """nastav hash na pin_hash a smaz pin"""
        if self.pin_code != "":
            self.pin_code_hash = make_password(self.pin_code)
        self.pin_code = ""

    def check_pin_code(self, pin_code) -> bool:
        """Kontrola pin_code"""
        return check_password(pin_code, self.pin_code_hash)

    def status_change(self) -> None:
        """pri zmene statusu vytovri novy zaznam v tabulce EmployeeStatusHistory"""
        if self.pk:
            old_status = Employee.objects.get(pk=self.pk).employee_status
            if old_status != self.employee_status:
                EmployeeStatusHistory.objects.create(
                    employee=self,
                    previous_status=old_status,
                    new_status=self.employee_status,
                    timestamp=now(),
                )

    def default_tables(self) -> None:
        """defaultni zaplneni tabulek"""
        # pokud v FK nic neni tak tam dej hodnotu PK klice z default
        if not self.employee_status:
            self.employee_status = EmployeeStatus.objects.get_or_create(
                name="free"
            )[0]
        if not self.department:
            self.department = Department.objects.get_or_create(
                name="nezarazeno"
            )[0]

    def save(self, *args, **kwargs) -> None:
        self.set_slug()  # nastav slug
        self.set_pin_hash()  # novy pinhash
        self.default_tables()  # kontrola tabulek
        self.status_change()  # zmena stavu na na history

        with tran.atomic():
            super().save(*args, **kwargs)

    class Meta:
        """Alphabetical"""

        ordering = ["surname"]


class FaceVector(models.Model):
    """Users picture table"""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="vector",
        verbose_name="Employee:",
    )

    face_vector = models.JSONField(
        unique=False,
        blank=True,
        null=False,
        verbose_name="Face vector:",
    )

    face_vector_fernet = models.BinaryField(
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="vector fernet:",
    )

    def __str__(self) -> str:
        return f"Face vector for {self.employee.slug}"

    def encrypt_vector(self) -> None:
        """encrypt vector"""
        if self.face_vector:
            to_fernet = dumps(self.face_vector).encode("utf-8")
            self.face_vector_fernet = fernet.encrypt(to_fernet)
        self.face_vector = []

    def decrypt_vector(self) -> str | None:
        """Decrypt the fernet vector"""
        if self.face_vector_fernet:
            decrypted_vector = fernet.decrypt(self.face_vector_fernet).decode()
            return decrypted_vector
        return None

    def compare_vectors(self, input_vector):
        """Compare input vector with the stored face vector."""
        decrypted_vector = self.decrypt_vector()
        if decrypted_vector:
            try:
                decrypted_vector_json = loads(decrypted_vector)
                input_vector_json = loads(input_vector)
                return decrypted_vector_json == input_vector_json
            except JSONDecodeError:
                return False
        return False

    def clean(self) -> None:
        """Validace dat"""
        if not self.face_vector_fernet or not self.employee.pin_code_hash:
            raise ValidationError("Face vector nebo pin hash neni v poradku")

    def save(
        self,
        *args,
        **kwargs,
    ):
        """Ukladani databaze"""
        self.encrypt_vector()

        self.employee.is_valid = bool(
            self.face_vector_fernet and self.employee.pin_code_hash
        )

        with tran.atomic():
            self.employee.save()
            super().save(*args, **kwargs)


class Department(models.Model):
    """Oddělení"""

    name = models.CharField(
        max_length=50,
        unique=True,
        default="nezarazeno",
        verbose_name="Název oddělení",
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        """Tridit podle"""

        ordering = ["id"]


class EmployeeStatus(models.Model):
    """Stav zaměstnance"""

    STATUS_CHOICES = [
        ("working", "V práci"),
        ("sick_leave", "Nemocenská"),
        ("business_trip", "Služební cesta"),
        ("vacation", "Dovolená"),
        ("free", "Volno"),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=STATUS_CHOICES,
        default="free",
        verbose_name="Stav",
    )

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"EmployeeStatus: {self.name}"


class EmployeeStatusHistory(models.Model):
    """Historie stavů zaměstnance."""

    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="status_history"
    )
    previous_status = models.ForeignKey(
        "EmployeeStatus",
        on_delete=models.SET_NULL,
        null=True,
        related_name="previous_statuses",
        verbose_name="predesly status",
    )
    new_status = models.ForeignKey(
        "EmployeeStatus",
        on_delete=models.SET_NULL,
        null=True,
        related_name="new_statuses",
        verbose_name="novy status",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"Historie stavu {self.employee.slug} - "
            f"{self.timestamp.strftime('%d.%m.%Y - %H:%M:%S')}"
        )

    class Meta:
        """ordering"""

        ordering = ["-timestamp"]
