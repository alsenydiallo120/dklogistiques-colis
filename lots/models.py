from django.db import models
from colis.models import Coli
from agences.models import Agence
from accounts.models import CustomUser

class Lot(models.Model):
    codelot = models.CharField(max_length=100)
    poids_lot = models.CharField(max_length=100)
    nombre_colis=models.IntegerField()
    dates=models.DateField(verbose_name="Date")
    heure=models.DateTimeField(auto_now_add=True)
    agences=models.ForeignKey(Agence,on_delete=models.SET_NULL, blank=False, null=True)
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL, blank=False, null=True)
    # ----------------------------ETAT LOT------------------------------------
    etat_embarqment=models.CharField(max_length=10,default=0)
    user_etat_embarqment=models.ForeignKey(CustomUser,related_name="user_etat_lot",on_delete=models.CASCADE,null=True,blank=True)
    date_etat_embarqment=models.DateField(null=True,blank=True)
    heure_etat_embarqment=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.codelot

    class Meta:
        db_table = "lots"

class DetailLot(models.Model):
    lots=models.ForeignKey(Lot,on_delete=models.CASCADE)
    colis=models.ForeignKey(Coli,on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.lots)

    class Meta:
        db_table = "detail_lots"
    
class CodeLot(models.Model):
    class Meta:
        db_table = "codelot"