# Generated by Django 4.1 on 2024-02-28 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('depenses', '0007_alter_depense_agences_alter_depense_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='depense',
            old_name='type',
            new_name='types',
        ),
    ]
