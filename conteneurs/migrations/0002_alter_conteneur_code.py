# Generated by Django 4.1 on 2024-02-28 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conteneurs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conteneur',
            name='code',
            field=models.CharField(error_messages={'unique': 'Ce code existe déjà'}, max_length=255, unique=True, verbose_name='Code du conteneur'),
        ),
    ]
