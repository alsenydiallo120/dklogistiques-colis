# Generated by Django 3.2 on 2022-11-30 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100, unique=True, verbose_name="Nom de l'agence")),
            ],
            options={
                'db_table': 'agences',
            },
        ),
    ]
