"""app-main Models"""

import os
from datetime import date
from json import JSONDecodeError, dumps, loads

import numpy as np
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import check_password, make_password
from django.core import validators as val
from django.db import models
from django.db import transaction as tran
from django.forms import ValidationError
from django.utils.text import slugify
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
key: str = os.getenv("FERNET_KEY", default="")
fernet = Fernet(key)

con: Console = Console()


class Employee(models.Model):
    """Employee"""

    name = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Jmeno:"
    )
    surname = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Prijmeni:"
    )
    street_number = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="Ulice/c.p.:"
    )
    city = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Mesto:"
    )

    postal_code = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        verbose_name="PSC:",
        validators=[
            val.MinLengthValidator(5),
            val.RegexValidator(
                regex=r"^\d{5}$", message="PSC musí obsahovat 5 číslic."
            ),
        ],
    )

    phone_number = models.CharField(
        max_length=16,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Telefon:",
        validators=[
            val.MinLengthValidator(5),
            val.RegexValidator(
                regex=r"^\+?[0-9\s\-()]{5,16}$",
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
        verbose_name="Datum narozeni:",
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
                message="PIN kód musí obsahovat přesně 4 číslice.",
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

    slug = models.SlugField(
        blank=True,
        unique=True,
        verbose_name="slug:",
    )

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    def __repr__(self) -> str:
        return f"Employee: {self.name} {self.surname} {self.status()}"

    def set_slug(self):
        """Vytvor slug"""
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.surname}")

    def status(self) -> str:
        """Status"""
        if self.is_valid:
            return "is valid"
        return "is invalid"

    def date_of_birth_format(self):
        """Datum narozeni formatovani"""
        if self.date_of_birth:
            return self.date_of_birth.strftime("%d. %m. %Y")
        return None

    def age(self):
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
        return None

    def set_pin_hash(self):
        """nastav hash na pin_hash a smaz pin"""
        if self.pin_code != "":
            self.pin_code_hash = make_password(self.pin_code)
        self.pin_code = ""

    def check_pin_code(self, pin_code):
        """Kontrola pin_code"""
        return check_password(pin_code, self.pin_code_hash)

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_pin_hash()

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

    def clean(self):
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
        max_length=50, unique=True, verbose_name="Název oddělení"
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        """Tridit podle"""

        ordering = ["name"]
