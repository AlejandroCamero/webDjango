# Generated by Django 3.1.2 on 2022-01-27 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0004_auto_20220123_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='dischargeDate',
            field=models.DateField(default=datetime.date(2022, 1, 27), verbose_name='Fecha de alta'),
        ),
        migrations.AlterField(
            model_name='project',
            name='finDate',
            field=models.DateField(verbose_name='Fecha de finalización'),
        ),
    ]