# Generated by Django 2.1.4 on 2019-01-18 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0004_kurs_sprzet'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosiadaSprzet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ilosc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UczestnikKursu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('potwierdzenie_wplaty', models.BinaryField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UczestnikWyjazdu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_zgloszenia', models.CharField(choices=[('oczek', 'Oczekujące'), ('odrz', 'Odrzucone'), ('zaakc', 'Zaakceptowane')], max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='sprzet',
            name='ilosc',
        ),
        migrations.AddField(
            model_name='kurs',
            name='instruktor',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.CASCADE, to='WebApp.Instruktor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wyjazd',
            name='organizator',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.CASCADE, to='WebApp.Wspinacz'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wspinacz',
            name='ubezpieczenie',
            field=models.FileField(blank=True, db_index=True, null=True, upload_to='uploads'),
        ),
        migrations.AddField(
            model_name='uczestnikwyjazdu',
            name='wspinacz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Wspinacz'),
        ),
        migrations.AddField(
            model_name='uczestnikwyjazdu',
            name='wyjazd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Wyjazd'),
        ),
        migrations.AddField(
            model_name='uczestnikkursu',
            name='kurs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Kurs'),
        ),
        migrations.AddField(
            model_name='uczestnikkursu',
            name='wspinacz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Wspinacz'),
        ),
        migrations.AddField(
            model_name='posiadasprzet',
            name='sprzet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Sprzet'),
        ),
        migrations.AddField(
            model_name='posiadasprzet',
            name='wspinacz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Wspinacz'),
        ),
    ]
