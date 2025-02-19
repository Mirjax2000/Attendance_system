"""Models"""

from datetime import date

from django.core import validators as val
from django.db import models
from django.db import transaction as tran
from django.utils.text import slugify


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

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    class Meta:
        """Alphabetical"""

        ordering = ["surname"]


class UserPicture(models.Model):
    """Users picture table"""

    PATH_TO_IMG: str = "media.employee_img"  # cesta k obrazkum pro DB

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="pictures",
        verbose_name="Zamestnanec: ",
    )
    image1 = models.ImageField(
        upload_to=PATH_TO_IMG, null=True, blank=False, verbose_name="img 1:"
    )
    image2 = models.ImageField(
        upload_to=PATH_TO_IMG, null=True, blank=False, verbose_name="img 2:"
    )
    image3 = models.ImageField(
        upload_to=PATH_TO_IMG, null=True, blank=False, verbose_name="img 3:"
    )

    def __str__(self):
        return f"Photos of {self.employee.name} {self.employee.surname}"

    def save(self, *args, **kwargs):
        """Ukladani souboru"""
        with tran.atomic():
            self.employee.is_valid = True
            self.employee.save()
            super().save(*args, **kwargs)
