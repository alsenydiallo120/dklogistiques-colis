# Generated by Django 3.2 on 2022-11-30 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tauxs', '0002_alter_taux_euro'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taux',
            options={'ordering': ['-id']},
        ),
    ]
