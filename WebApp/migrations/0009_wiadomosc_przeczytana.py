# Generated by Django 2.1.4 on 2019-01-18 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0008_wiadomosc_tytul'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiadomosc',
            name='przeczytana',
            field=models.BooleanField(default=False),
        ),
    ]
