from datetime import datetime, date

from django.db.models import Model, CharField, DateField, IntegerField, \
    BooleanField, OneToOneField, ImageField, CASCADE


class Employee(Model):
    name = CharField(max_length=32, null=False, blank=False)
    surname = CharField(max_length=32, null=False, blank=False)
    street_number = CharField(max_length=50, null=False, blank=False)
    city = CharField(max_length=32, null=False, blank=False)
    postal_code = IntegerField(null=False, blank=False)
    phone_number = CharField(max_length=16, unique=True, null=False, blank=False)
    email = CharField(max_length=100, unique=True, null=False, blank=False)
    date_of_birth = DateField(null=False, blank=False)
    is_valid = BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname}"

    def __repr__(self):
        return f"Employee: {self.name} {self.surname} {self.status()}"

    def status(self):
        if self.is_valid:
            return f"is valid"
        else:
            return f"is invalid"

    def date_of_birth_format(self):
        if self.date_of_birth:
            return datetime.strftime(self.date_of_birth, "%d. %m. %Y")
        return None

    def age(self):
        if self.date_of_birth:
            end_date = date.today()
            return (end_date - self.date_of_birth).days // 365
        return None

    class Meta:
        ordering = ['surname']


class UserPicture(Model):
    employee = OneToOneField(Employee, on_delete=CASCADE, related_name="pictures")
    image1 = ImageField(upload_to='user_pictures/', null=False, blank=False)
    image2 = ImageField(upload_to='user_pictures/', null=False, blank=False)
    image3 = ImageField(upload_to='user_pictures/', null=False, blank=False)

    def __str__(self):
        return f"Photos of {self.employee.name} {self.employee.surname}"

    def save_photos(self):
        self.employee.is_valid = True
        self.employee.save()
        super().save()
