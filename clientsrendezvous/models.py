from django.db import models
from autoslug import AutoSlugField
import secrets


ASCENSEUR = (
    ('',"L'appartement contient-il un ascenseur"),
    ('Oui','Oui'),
    ('Non', 'Non'),
)

class Clientsrendezvou(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Prénom et nom")
    telephone = models.CharField(max_length=100, verbose_name="Téléphone",unique=True,error_messages={"unique":"Ce numéro existe déjà"})
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    rue = models.CharField(max_length=255, verbose_name="Rue", blank=True, null=True)
    code_postal = models.CharField(max_length=255, verbose_name="Code postal", blank=True, null=True)
    ville = models.CharField(max_length=255, verbose_name="Ville", blank=True, null=True)
    etage = models.CharField(max_length=255, verbose_name="Étage", blank=True, null=True)
    code = models.CharField(max_length=255, verbose_name="Code d'accès", blank=True, null=True)
    num_app = models.CharField(max_length=255, verbose_name="N° de l'appartement", blank=True, null=True)
    ascenseur=models.CharField(max_length=255,choices=ASCENSEUR, blank=True, null=True)
    slug = AutoSlugField(unique=True,editable=False)  


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = "clientsrendezvous"
    