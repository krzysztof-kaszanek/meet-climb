# Generated by Django 2.1.4 on 2019-01-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0011_auto_20190119_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='kurs',
            name='limit_osob',
            field=models.PositiveIntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uczestnikkursu',
            name='potwierdzenie_wplaty',
            field=models.FileField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
