# Generated by Django 4.1 on 2024-04-14 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_customuser_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='types',
            field=models.CharField(blank=True, choices=[('', 'Séléctionner le type'), ('Vol', 'Vol'), ('Bateau', 'Bateau')], max_length=255, null=True),
        ),
    ]
