# Generated by Django 5.1.6 on 2025-03-23 12:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_main", "0013_alter_employee_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="pin_code",
            field=models.CharField(
                max_length=4,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_pin",
                        message="PIN kód musí obsahovat přesně 4 číslice.",
                        regex="^\\d{4}$",
                    )
                ],
                verbose_name="PIN kod:",
            ),
        ),
    ]
