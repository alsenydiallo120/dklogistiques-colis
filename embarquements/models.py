from django.db import models
from colis.models import Coli
from agences.models import Agence
from accounts.models import CustomUser
from lots.models import Lot
from transporteurs.models import Transporteur

class Embarquement(models.Model):
    codeembarquement = models.CharField(max_length=255,verbose_name="")
    poids_embarquement = models.CharField(max_length=255,verbose_name="")
    transporteurs=models.ForeignKey(Transporteur,on_delete=models.SET_NULL,null=True,blank=False)
    poids = models.CharField(max_length=255)
    nombre_lots = models.CharField(max_length=255)
    etat_reception = models.CharField(max_length=255,default=0,null=True,blank=True)
    dates=models.DateField(verbose_name="Date")
    heure=models.DateTimeField(auto_now_add=True)
    agence_depart=models.ForeignKey(Agence,on_delete=models.SET_NULL,null=True,blank=False,related_name="agence3")
    agence_arrive=models.ForeignKey(Agence,on_delete=models.SET_NULL,null=True,blank=False,related_name="agence4",verbose_name="Agence de destination")
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=False)

    def __str__(self):
        return self.codeembarquement

    class Meta:
        db_table = "embarquements"

    
class CodeEmbarquement(models.Model):
    class Meta:
        db_table = "code_embarquements"
    
class DetailEmbarquement(models.Model):
    embarquements=models.ForeignKey(Embarquement,on_delete=models.CASCADE)
    lots=models.ForeignKey(Lot,on_delete=models.CASCADE)
    