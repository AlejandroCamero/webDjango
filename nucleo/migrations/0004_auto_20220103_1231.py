# Generated by Django 3.1.2 on 2022-01-03 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0003_auto_20220103_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='active',
            field=models.IntegerField(default=0, verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='client',
            name='dischargeDate',
            field=models.DateField(null=True, verbose_name='Fecha de alta'),
        ),
    ]
