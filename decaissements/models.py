from django.db import models
from accounts.models import CustomUser
from agences.models import Agence

DEVISE = (
    ('€','€'),
    ('gnf', 'GNF'),
)

class Decaissement(models.Model):
    montant=models.DecimalField(verbose_name="Montant",max_digits=65,decimal_places=2)
    devise=models.CharField(max_length=255,verbose_name="Dévise",choices=DEVISE)
    dates=models.DateField(verbose_name="Date")
    emetteur=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=False, null=True,related_name="emetteur")
    recepteur=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=False, null=True,related_name="recepteur",verbose_name="Recepteur")
    agences=models.ForeignKey(Agence,on_delete=models.SET_NULL,blank=False, null=True)
    motif = models.CharField(max_length=255,verbose_name="Motif")
    created_at=models.DateTimeField(auto_now_add=True)
    etat=models.BooleanField(default=0,verbose_name="")
    validate_by=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=False, null=True,related_name="validate_by")


    def __str__(self):
        return self.montant

    class Meta:
        db_table = "decaissements"

 
    