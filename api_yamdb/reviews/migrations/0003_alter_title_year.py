# Generated by Django 3.2 on 2023-09-14 15:57

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_remove_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[api.utils.validate_year_field], verbose_name='Год выпуска'),
        ),
    ]
