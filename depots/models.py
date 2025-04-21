from django.db import models
from accounts.models import CustomUser
from agences.models import Agence
DEVISE = (
    ('€','€'),
    ('gnf', 'GNF'),
)

class Depot(models.Model):
    montant=models.CharField(max_length=255,verbose_name="Montant déposé")
    devise=models.CharField(max_length=255,verbose_name="Dévies",choices=DEVISE)
    dates=models.DateField(verbose_name="Date")
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    agences=models.ForeignKey(Agence,on_delete=models.CASCADE)
    motif = models.CharField(max_length=255,verbose_name="Motif")

    def __str__(self):
        return self.montant

    class Meta:
        db_table = "depots"

    def save(self, *args, **kwargs):
        self.montant=self.montant.replace(",","")
        super().save(*args, **kwargs)
    