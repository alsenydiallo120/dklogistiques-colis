from django.db import models
from autoslug import AutoSlugField
import secrets
from clientsrendezvous.models import Clientsrendezvou
from chauffeurs.models import Chauffeur


ASCENSEUR = (
    ('',"L'appartement contient-il un ascenseur"),
    ('Oui','Oui'),
    ('Non', 'Non'),
)

class Rendezvou(models.Model):
    clients=models.ForeignKey(Clientsrendezvou,on_delete=models.SET_NULL,null=True,blank=False)
    dates = models.DateField(verbose_name="Date de rendez-vous")
    heure_debut = models.TimeField(verbose_name="Debut")
    heure_fin = models.TimeField(verbose_name="Fin")
    slug = AutoSlugField(unique=True,editable=False)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.clients.nom

    class Meta:
        db_table = "rendezvous"
    

class PriseRendezvou(models.Model):
    rendezvous=models.ForeignKey(Rendezvou,on_delete=models.CASCADE,null=True,blank=False)
    chauffeurs=models.ForeignKey(Chauffeur,on_delete=models.CASCADE,null=True,blank=False)
    dates=models.DateTimeField(auto_now_add=True)
    datejour=models.DateField()
    slug = AutoSlugField(unique=True,editable=False)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.rendezvous)

    class Meta:
        db_table = "prise_rendezvous"





class RendezvousMobile(models.Model):
    nom=models.CharField(max_length=255,verbose_name='Nom complet')
    telephone=models.CharField(max_length=255,verbose_name="N° de Téléphone")
    email=models.EmailField()
    date = models.DateField(verbose_name="Date du rendez-vous")
    heure = models.TimeField(verbose_name="Heure du rendez-vous")
    description=models.TextField(null=True,blank=False)
    slug = AutoSlugField(unique=True,editable=False)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = "rendezvous_mobiles"
    