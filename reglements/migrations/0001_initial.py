# Generated by Django 4.1 on 2024-02-23 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agences', '0003_remove_agence_adresse'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('colis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reglement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reste_euro', models.CharField(max_length=255, verbose_name='Reste à payé en Euro')),
                ('reste_gnf', models.CharField(blank=True, max_length=255, null=True, verbose_name='Reste à payé en GNF')),
                ('montant', models.CharField(max_length=255, verbose_name='Montant payé')),
                ('recupe_par', models.CharField(max_length=255, verbose_name='Recuperé par')),
                ('telephone', models.CharField(max_length=255, verbose_name='Téléphone de la personne qui recuperé')),
                ('devise', models.CharField(choices=[('€', '€'), ('gnf', 'GNF')], max_length=255)),
                ('lieu', models.CharField(choices=[('paris', 'Payé à Paris'), ('guinee', 'Payé en Guinée')], max_length=255)),
                ('dates', models.DateField(verbose_name='Date')),
                ('agences', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agences.agence')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('colis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colis.coli')),
            ],
            options={
                'db_table': 'reglements',
            },
        ),
    ]
