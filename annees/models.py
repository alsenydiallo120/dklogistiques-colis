from django.db import models

class Annee(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="Année")
    lettre = models.CharField(max_length=100, unique=True, verbose_name="Lettre de l'année pour les bateaux")

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = "annees"
    