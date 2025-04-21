from django.db import models
from django.contrib.auth.models import AbstractUser
from agences.models import Agence


TYPE = (
    ('','Séléctionner le type'),
    ('Vol','Vol'),
    ('Bateau', 'Bateau'),
)

class CustomUser(AbstractUser):
    nom = models.CharField(max_length=100, blank=False, null=True,verbose_name="Prenom et nom")
    telephone = models.IntegerField(blank=False, null=True,unique=True)
    email = models.EmailField(blank=True, null=True,unique=True)
    agences=models.ForeignKey(Agence,on_delete=models.CASCADE,verbose_name="Agence",null=True,blank=True)
    taux_jour = models.CharField(max_length=100,blank=True, null=True)
    valeur_taux = models.CharField(max_length=100,blank=True, null=True)
    types=models.CharField(max_length=255,choices=TYPE,blank=True, null=True)

    class Meta:
        db_table = "accounts"
    
    def __str__(self):
        return str(self.nom or "")+" "+str(self.telephone or "")
    
