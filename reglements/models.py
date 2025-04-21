from django.db import models
from annees.models import Annee
from pays.models import Pay
from accounts.models import CustomUser
from agences.models import Agence
from colis.models import Coli, ColiBateau

DEVISE = (
    ('€','€'),
    ('gnf', 'GNF'),
)

LIEU = (
    ('paris','Payé à Paris'),
    ('guinee', 'Payé en Guinée'),
)

class Reglement(models.Model):
    reference=models.CharField(max_length=255,verbose_name='')
    colis=models.ForeignKey(Coli,on_delete=models.CASCADE,blank=True, null=True)
    colisbateau=models.ForeignKey(ColiBateau,on_delete=models.CASCADE,blank=True, null=True)
    reste_euro=models.CharField(max_length=255,verbose_name="Reste à payé en Euro")
    reste_gnf=models.CharField(max_length=255,verbose_name="Reste à payé en GNF",null=True,blank=True)
    montant_euro=models.CharField(max_length=255,verbose_name="Montant payé en Euro",null=True,blank=True)
    montant_gnf=models.CharField(max_length=255,verbose_name="Montant payé en GNF",blank=True, null=True)
    recupe_par=models.CharField(max_length=255,verbose_name="Recuperé par")
    telephone=models.CharField(max_length=255,verbose_name="Téléphone de la personne qui recuperé")
    devise=models.CharField(max_length=255,choices=DEVISE,blank=True, null=True)
    lieu=models.CharField(max_length=255,choices=LIEU)
    dates=models.DateField(verbose_name="Date")
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=False,null=True)
    agences=models.ForeignKey(Agence,on_delete=models.SET_NULL,blank=False,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.reference

    class Meta:
        db_table = "reglements"

    def save(self, *args, **kwargs):
        if self.montant_euro is not None:  
            self.montant_euro=self.montant_euro.replace(",","")
        if self.montant_gnf is not None:
            self.montant_gnf=self.montant_gnf.replace(",","")
        super().save(*args, **kwargs)


class ReferenceReception(models.Model):
    annees=models.ForeignKey(Annee,on_delete=models.SET_NULL,blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = "reference_reception"
