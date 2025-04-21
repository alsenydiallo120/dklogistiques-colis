from django.db import models

class Transporteur(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Prénom et nom du transporteur")
    telephone = models.CharField(max_length=100, unique=True, verbose_name="Téléphone")

    def __str__(self):
        return self.nom+" | "+self.telephone

    class Meta:
        db_table = "transporteurs"
    