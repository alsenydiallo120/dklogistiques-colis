from django.db import models

# Create your models here.

class Typecompte(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="Libelle")
    statut = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = "typecomptes"
    