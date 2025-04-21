from django.db import models
from autoslug import AutoSlugField
import secrets

class Chauffeur(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Prénom et nom")
    telephone = models.CharField(max_length=100, unique=True, verbose_name="Téléphone",error_messages={"unique":"Ce numéro existe déjà"})
    slug = AutoSlugField(unique=True,editable=False)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom+" | "+self.telephone

    class Meta:
        db_table = "chauffeurs"
    