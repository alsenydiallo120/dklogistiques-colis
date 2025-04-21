from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Entreprise(models.Model):
    nom=models.CharField(max_length=255,verbose_name="Nom de l'entreprise",null=True,blank=True)
    abreviation=models.CharField(max_length=255,verbose_name="Abreviation",null=True,blank=True)
    logo=models.ImageField(upload_to="logo",verbose_name="logo de l'entreprise")
    email=models.EmailField(max_length=255,verbose_name="Email",null=True,blank=True)
    site=models.CharField(max_length=255,verbose_name="Site Web",null=True,blank=True)
    rccm=models.CharField(max_length=255,verbose_name="RCCM",null=True,blank=True)
    telephone_paris=models.CharField(max_length=255,verbose_name="Téléphone Paris",null=True,blank=True)
    telephone_guinee=models.CharField(max_length=255,verbose_name="Téléphone Guinée",null=True,blank=True)
    adresse_paris=models.CharField(max_length=255,verbose_name="Adresse Paris",null=True,blank=True)
    adresse_guinee=models.CharField(max_length=255,verbose_name="Adresse Guinée",null=True,blank=True)
    services=models.TextField(null=True,blank=True)

    class Meta:
        db_table="entreprise"
    
    def __str__(self):
        return self.logo
    



