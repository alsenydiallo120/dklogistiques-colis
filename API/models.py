from django.db import models
from colis.models import Coli
from autoslug import AutoSlugField
import secrets


class Scanner(models.Model):
    colis = models.ForeignKey(Coli,on_delete=models.CASCADE)
    class Meta:
        db_table = "scanner"


class Demandedevis(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Prénom et nom")
    telephone = models.CharField(max_length=100, verbose_name="Téléphone")
    email = models.EmailField(max_length=100, verbose_name="Email")
    adresse=models.CharField(max_length=255,verbose_name='Adresse')
    poids=models.CharField(max_length=255,verbose_name='Poids')
    description=models.CharField(max_length=255,verbose_name='Description')
    slug = AutoSlugField(unique=True,editable=False)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "damandedevis"
    