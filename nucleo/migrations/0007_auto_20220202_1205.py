# Generated by Django 3.1.2 on 2022-02-02 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0006_auto_20220201_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='dischargeDate',
            field=models.DateField(default=datetime.date(2022, 2, 2), verbose_name='Fecha de alta'),
        ),
    ]
