# Generated by Django 4.1 on 2024-04-18 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annees', '0001_initial'),
        ('regulations', '0005_referenceregulation_regulation_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenceregulation',
            name='annees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='annees.annee'),
        ),
    ]
