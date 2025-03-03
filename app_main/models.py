"""Models"""

import os
from datetime import date
from json import dumps

from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
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
        max_length=32, null=False, blank=False, verbose_name="Jmeno: "
    )
    surname = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Prijmeni: "
    )
    street_number = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="Ulice/c.p.: "
    )
    city = models.CharField(
        max_length=32, null=False, blank=False, verbose_name="Mesto: "
    )

    postal_code = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        verbose_name="PSC: ",
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
        verbose_name="Telefon: ",
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
        verbose_name="Email: ",
    )
    date_of_birth = models.DateField(
        null=False,
        blank=False,
        verbose_name="Datum narozeni: ",
    )
    is_valid = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Ucet v poradku?: ",
    )
    pin_code = models.CharField(
        max_length=4,
        blank=True,
        null=False,
        verbose_name="PIN kod: ",
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

    slug = models.SlugField(
        blank=True,
        unique=True,
        verbose_name="slug: ",
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
            end_date = date.today()
            return (end_date - self.date_of_birth).days // 365
        return None

    def set_pin_hash(self):
        """nastav hash na pin_hash a smaz pin"""
        if self.pin_code != "":
            self.pin_code_hash = make_password(self.pin_code)
            self.pin_code = ""
        else:
            con.log("update formulare s prazdnym hashem")

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
        verbose_name="Zamestnanec: ",
    )

    face_vector = models.JSONField(
        unique=False, blank=False, null=False, verbose_name="Face vector: "
    )

    face_vector_fernet = models.TextField(
        unique=False, blank=True, null=False, verbose_name="vector fernet:"
    )

    def __str__(self):
        return f"Face vector for {self.employee.name} {self.employee.surname}"

    def fernet_vector(self):
        """sifruj vector"""
        if self.face_vector:
            to_fernet = dumps(self.face_vector).encode("utf-8")
            self.face_vector_fernet = fernet.encrypt(to_fernet)
            self.face_vector = []

    def save(
        self,
        *args,
        **kwargs,
    ):
        """Ukladani souboru"""
        self.fernet_vector()

        if self.face_vector_fernet and self.employee.pin_code_hash:
            self.employee.is_valid = True
        else:
            self.employee.is_valid = False
            raise ValidationError("Face vector nebo pin hash neni v poradku")
        with tran.atomic():
            self.employee.save()
            super().save(*args, **kwargs)
