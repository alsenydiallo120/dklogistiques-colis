from django.db import models
from pays.models import Pay
from accounts.models import CustomUser
from agences.models import Agence
from colis.models import *
from annees.models import Annee


class Regulationbateau(models.Model):
    reference=models.CharField(max_length=255,verbose_name='')
    colis=models.ForeignKey(ColiBateau,on_delete=models.CASCADE,verbose_name="Code du colis")
    reste=models.DecimalField(verbose_name="Reste à payé",decimal_places=2,max_digits=65,editable=False,blank=True, null=True)
    montant=models.DecimalField(verbose_name="Montant payé",decimal_places=2,max_digits=65)
    dates=models.DateField(verbose_name="Date")
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=True,null=True,editable=False)
    agences=models.ForeignKey(Agence,on_delete=models.SET_NULL,blank=True,null=True,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True,blank=True,editable=False)

    def __str__(self):
        return self.montant

    class Meta:
        db_table = "regulationbateaus"


class ReferenceRegulationBateau(models.Model):
    annees=models.ForeignKey(Annee,on_delete=models.SET_NULL,blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = "reference_reglement_bateau"


    