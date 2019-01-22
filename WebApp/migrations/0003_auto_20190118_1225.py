# Generated by Django 2.1.4 on 2019-01-18 11:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0002_instruktor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wyjazd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_rozpoczecia', models.DateField()),
                ('data_zakonczenia', models.DateField()),
                ('tytul', models.CharField(max_length=255)),
                ('opis', models.CharField(max_length=255)),
                ('trudnosci_drog', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('3', '3'), ('4', '4'), ('5a', '5a'), ('5b', '5b'), ('5c', '5c'), ('6a', '6a'), ('6b', '6b'), ('6c', '6c'), ('7a', '7a'), ('7b', '7b'), ('7c', '7c'), ('8a', '8a'), ('8b', '8b'), ('8c', '8c'), ('9a', '9a'), ('9b', '9b'), ('9c', '9c')], max_length=255), size=None)),
            ],
        ),
        migrations.AlterField(
            model_name='instruktor',
            name='stopien_instruktorski',
            field=models.CharField(choices=[('wsp_skalnej', 'Instruktor wspinaczki skalnej'), ('tater', 'Instruktor taternictwa'), ('alp', 'Instruktor alpinizmu')], max_length=255),
        ),
        migrations.AlterField(
            model_name='wspinacz',
            name='ubezpieczenie',
            field=models.BinaryField(null=True),
        ),
    ]