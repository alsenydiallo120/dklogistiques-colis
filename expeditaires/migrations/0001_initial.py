# Generated by Django 3.2 on 2022-11-30 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expeditaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name="Prénom et nom de l'expeditaire")),
                ('telephone', models.CharField(max_length=100, unique=True, verbose_name='Téléphone')),
            ],
            options={
                'db_table': 'expeditaires',
            },
        ),
    ]
