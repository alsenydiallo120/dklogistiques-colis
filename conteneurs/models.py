from django.db import models
from annees.models import Annee
from pays.models import Pay


class Conteneur(models.Model):
    code = models.CharField(max_length=255,verbose_name="Code du conteneur")
    annees=models.ForeignKey(Annee,on_delete=models.SET_NULL,null=True,blank=False)
    cloture=models.BooleanField(default=False,verbose_name="Cloturé ?")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "conteneurs"
        unique_together=["code","annees"]


class RefConteneur(models.Model):
    class Meta:
        db_table = "ref_conteneurs"
    