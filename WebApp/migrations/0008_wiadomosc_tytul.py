# Generated by Django 2.1.4 on 2019-01-18 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0007_wiadomosc'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiadomosc',
            name='tytul',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]