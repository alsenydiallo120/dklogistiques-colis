# Generated by Django 4.1.6 on 2023-06-06 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_agences'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='valeur_taux',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
