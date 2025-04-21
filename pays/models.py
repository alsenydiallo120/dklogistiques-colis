from django.db import models

class Pay(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="Nom du pays")

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = "pays"
    