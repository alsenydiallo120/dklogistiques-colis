from django.db import models

class Expeditaire(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Prénom et nom de l'expeditaire")
    telephone = models.CharField(max_length=100, unique=True, verbose_name="Téléphone")

    def __str__(self):
        return self.nom

    class Meta:
        db_table = "expeditaires"
    