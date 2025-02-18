"""Models"""

from datetime import date, datetime

from django.core.validators import EmailValidator
from django.db import transaction
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    ImageField,
    IntegerField,
    Model,
    OneToOneField,
)


class Employee(Model):
    """Employee"""

    name = CharField(
        max_length=32, null=False, blank=False, verbose_name="Jmeno: "
    )
    surname = CharField(
        max_length=32, null=False, blank=False, verbose_name="Prijmeni: "
    )
    street_number = CharField(
        max_length=50, null=False, blank=False, verbose_name="Ulice/c.p.: "
    )
    city = CharField(
        max_length=32, null=False, blank=False, verbose_name="Mesto: "
    )
    postal_code = IntegerField(null=False, blank=False, verbose_name="PSC: ")
    phone_number = CharField(
        max_length=16,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Telefon: ",
    )
    email = CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Email: ",
        validators=[EmailValidator()],
    )
    date_of_birth = DateField(
        null=False,
        blank=False,
        verbose_name="Datum narozeni: ",
    )
    is_valid = BooleanField(
        default=False,
        verbose_name="Ucet v poradku?: ",
    )

    def __str__(self):
        return f"{self.name} {self.surname}"

    def __repr__(self):
        return f"Employee: {self.name} {self.surname} {self.status()}"

    def status(self):
        """Status"""
        if self.is_valid:
            return "is valid"
        else:
            return "is invalid"

    def date_of_birth_format(self):
        """Datum narozeni formatovani"""
        if self.date_of_birth:
            return datetime.strftime(self.date_of_birth, "%d. %m. %Y")
        return None

    def age(self):
        """Vypocet veku"""
        if self.date_of_birth:
            end_date = date.today()
            return (end_date - self.date_of_birth).days // 365
        return None

    class Meta:
        """Alphabetical"""

        ordering = ["surname"]


class UserPicture(Model):
    """Users picture table"""

    PATH_TO_IMG: str = "media.employee_img"  # cesta k obrazkum pro DB

    employee = OneToOneField(
        Employee,
        on_delete=CASCADE,
        related_name="pictures",
        verbose_name="Zamestnanec: ",
    )
    image1 = ImageField(
        upload_to=PATH_TO_IMG, null=False, blank=False, verbose_name="img 1: "
    )
    image2 = ImageField(
        upload_to=PATH_TO_IMG, null=False, blank=False, verbose_name="img 2:"
    )
    image3 = ImageField(
        upload_to=PATH_TO_IMG, null=False, blank=False, verbose_name="img 3:"
    )

    def __str__(self):
        return f"Photos of {self.employee.name} {self.employee.surname}"

    def save_photos(self):
        """Ukladani souboru"""
        with transaction.atomic():
            self.employee.is_valid = True
            self.employee.save()
            super().save()
