# Generated by Django 3.2 on 2023-09-13 19:00

import django.core.validators
from django.db import migrations, models

import api.utils


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                help_text='Укажите логин',
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message='Username doesnt comply',
                        regex='^[\\w.@+-]+\\Z',
                    ),
                    api.utils.validate_username_field,
                ],
                verbose_name='Логин',
            ),
        ),
    ]