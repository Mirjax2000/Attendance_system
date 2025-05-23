# Generated by Django 5.1.6 on 2025-03-15 14:03

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Název oddělení')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Jméno:')),
                ('surname', models.CharField(max_length=32, verbose_name='Příjmení:')),
                ('street_number', models.CharField(max_length=50, verbose_name='Ulice/č.p.:')),
                ('city', models.CharField(max_length=32, verbose_name='Město:')),
                ('postal_code', models.CharField(max_length=5, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.RegexValidator(message='PSČ musí obsahovat 5 číslic.', regex='^\\d{5}$')], verbose_name='PSČ:')),
                ('phone_number', models.CharField(max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.RegexValidator(message='Telefon musí být ve správném formátu.', regex='^\\+?[0-9\\s\\-()]{5,16}$')], verbose_name='Telefon:')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email:')),
                ('date_of_birth', models.DateField(verbose_name='Datum narození:')),
                ('is_valid', models.BooleanField(blank=True, default=False, verbose_name='Ucet v poradku?:')),
                ('pin_code', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(code='invalid_pin', message='PIN kód musí obsahovat přesně 4 číslice.', regex='^\\d{4}$')], verbose_name='PIN kod:')),
                ('pin_code_hash', models.CharField(blank=True, max_length=255, verbose_name='Pin Hash:')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='slug:')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_main.department', verbose_name='Oddělení')),
            ],
            options={
                'ordering': ['surname'],
            },
        ),
        migrations.CreateModel(
            name='FaceVector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_vector', models.JSONField(blank=True, verbose_name='Face vector:')),
                ('face_vector_fernet', models.BinaryField(blank=True, db_index=True, null=True, unique=True, verbose_name='vector fernet:')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vector', to='app_main.employee', verbose_name='Employee:')),
            ],
        ),
    ]
