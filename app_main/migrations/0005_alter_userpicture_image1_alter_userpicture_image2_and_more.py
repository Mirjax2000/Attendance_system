# Generated by Django 5.1.6 on 2025-02-18 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_main", "0004_alter_employee_phone_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userpicture",
            name="image1",
            field=models.ImageField(
                null=True, upload_to="media.employee_img", verbose_name="img 1:"
            ),
        ),
        migrations.AlterField(
            model_name="userpicture",
            name="image2",
            field=models.ImageField(
                null=True, upload_to="media.employee_img", verbose_name="img 2:"
            ),
        ),
        migrations.AlterField(
            model_name="userpicture",
            name="image3",
            field=models.ImageField(
                null=True, upload_to="media.employee_img", verbose_name="img 3:"
            ),
        ),
    ]
