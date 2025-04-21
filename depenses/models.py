from django.db import models
from pays.models import Pay
from accounts.models import CustomUser
from agences.models import Agence
from conteneurs.models import Conteneur


TYPE = (
    ('','Séléctionner le type'),
    ('Vol','Vol'),
    ('Bateau', 'Bateau'),
)


class Depense(models.Model):
    dates=models.DateField(verbose_name="Date")
    montant=models.DecimalField(verbose_name="Montant depensée",decimal_places=2,max_digits=65)
    devise=models.CharField(max_length=255)
    conteneurs=models.ForeignKey(Conteneur,on_delete=models.SET_NULL,null=True,blank=False)
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL, blank=False, null=True)
    agences=models.ForeignKey(Agence,on_delete=models.SET_NULL,blank=False, null=True)
    motif = models.TextField(verbose_name="Motif")

    def __str__(self):
        return str(self.montant)

    class Meta:
        db_table = "depenses"

    def save(self, *args, **kwargs):
        if not self.pk:
            if "guinee" in self.agences.pays.libelle.lower():
                self.devise = "gnf"
            elif "fran" in self.agences.pays.libelle.lower():
                self.devise = "€"
        super().save(*args, **kwargs)
    