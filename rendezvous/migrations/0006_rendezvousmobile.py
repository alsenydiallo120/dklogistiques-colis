# Generated by Django 4.1 on 2025-01-07 18:44

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendezvous', '0005_priserendezvou_datejour_priserendezvou_dates_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RendezvousMobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom complet')),
                ('telephone', models.CharField(max_length=255, verbose_name='N° de Téléphone')),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField(verbose_name='Date du rendez-vous')),
                ('heure_debut', models.TimeField(verbose_name='Heure du rendez-vous')),
                ('description', models.TextField(null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique=True)),
            ],
            options={
                'db_table': 'rendezvous_mobiles',
            },
        ),
    ]
