from django.db import models
from pays.models import Pay

class Agence(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="Nom de l'agence")
    pays=models.ForeignKey(Pay,on_delete=models.CASCADE,verbose_name="Pays")

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = "agences"
    