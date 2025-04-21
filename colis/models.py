from decimal import Decimal
import re
from django.db import models
from agences.models import Agence
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.conf import settings
from clients.models import Client
from conteneurs.models import Conteneur
from tauxs.models import Taux
from django.core.validators import MinValueValidator
CurrentUser = settings.AUTH_USER_MODEL
User = get_user_model()

DEVISE = (
    ('€','€'),
    ('gnf', 'GNF'),
)

class BaseColis(models.Model):
    code = models.CharField(max_length=255, verbose_name="Code",unique=True,error_messages={"unique":"Ce code existe déjà, valider à nouveau"},db_index=True)
    poids=models.DecimalField(max_digits=19, decimal_places=2,verbose_name="Poids",validators=[MinValueValidator(0)])
    prix = models.DecimalField(verbose_name="Prix du kilo en Euro",max_digits=19, decimal_places=2,validators=[MinValueValidator(0)])
    contenu=models.CharField(max_length=255,null=True,blank=False)
    devise = models.CharField(verbose_name='Devise',max_length=100,choices=DEVISE)
    nombre_colis = models.PositiveIntegerField(verbose_name="Nombre de colis")
    montant=models.DecimalField(max_digits=19, decimal_places=2)
    montant_euro=models.DecimalField(max_digits=19, decimal_places=2,null=True,blank=True)
    prix_euro=models.DecimalField(max_digits=19, decimal_places=2,null=True,blank=True)
    agence_depart=models.ForeignKey(Agence,on_delete=models.SET_NULL,related_name="%(class)s_agence1",null=True,blank=True)
    agence_arrive=models.ForeignKey(Agence,on_delete=models.SET_NULL,related_name="%(class)s_agence2",null=True,blank=True)
    expditaire=models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=False,related_name="%(class)s_Expeditaire")
    destinataire=models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=False,related_name="%(class)s_Destinataire")
    montant_paye=models.DecimalField(max_digits=19, decimal_places=2,verbose_name="Montant payé",null=True,blank=True)
    reste=models.DecimalField(max_digits=19, decimal_places=2,verbose_name="Reste",null=True,blank=True)
    devise_montantpaye=models.CharField(verbose_name="Dévise",max_length=100,choices=DEVISE)
    dates=models.DateField(verbose_name="Date",null=True,blank=True)
    heure=models.DateTimeField(auto_now_add=True)
    montant_euro=models.CharField(max_length=100, verbose_name="Montant en Euro",null=True,blank=True)
    montant_gnf=models.CharField(max_length=100, verbose_name="Montant en GNF",null=True,blank=True)
    total_paye=models.CharField(max_length=100, verbose_name="Total paye",null=True,blank=True)
    # -------------------------ENREGISTREMEMT----------------------------
    etat_enregistrement=models.CharField(max_length=10,default=1)
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=False)
    date_enregistrement=models.DateField(null=True,blank=True)
    heure_enregistrement=models.DateTimeField(null=True,blank=True)
    # -------------------------MISE EN LOT----------------------------
    etat_lot=models.CharField(max_length=10,default=0)
    user_lot=models.ForeignKey(User,related_name="%(class)s_user2",on_delete=models.SET_NULL,null=True,blank=True)
    date_lot=models.DateField(null=True,blank=True)
    heure_lot=models.DateTimeField(null=True,blank=True)
    # -------------------------EMBARQUEMENT----------------------------
    etat_embarquement=models.CharField(max_length=10,default=0)
    user_embarquement=models.ForeignKey(User,related_name="%(class)s_user3",on_delete=models.SET_NULL,null=True,blank=True)
    date_embarquement=models.DateField(null=True,blank=True)
    heure_embarquement=models.DateTimeField(null=True,blank=True)
    # -------------------------VERIFICATION----------------------------
    etat_verification=models.CharField(max_length=10,default=0)
    user_verification=models.ForeignKey(User,related_name="%(class)s_user4",on_delete=models.SET_NULL,null=True,blank=True)
    date_verification=models.DateField(null=True,blank=True)
    heure_verification=models.DateTimeField(null=True,blank=True)
    # -------------------------RECEPTION----------------------------
    etat_receptionclient=models.CharField(max_length=10,default=0)
    user_receptionclient=models.ForeignKey(User,related_name="%(class)s_user5",on_delete=models.SET_NULL,null=True,blank=True)
    date_receptionclient=models.DateField(null=True,blank=True)
    heure_receptionclient=models.DateTimeField(null=True,blank=True)
    montant_reglement=models.IntegerField(verbose_name="Montant",null=True,blank=True)
    devise_reglement=models.CharField(verbose_name="Dévise",max_length=100,choices=DEVISE)
    taux=models.CharField(max_length=100,null=True,blank=True)
    types=models.CharField(max_length=255,null=True,blank=True)
   
    def save(self, *args, **kwargs):     
        poids=float(self.poids)
        if self.montant_paye==None:
            montant_paye=0
        else:
            montant_paye=str(float(self.montant_paye)).replace(" ","")
        if poids<1:
            poids=1
        self.montant=self.prix*Decimal(str(poids))      
        self.montant_paye=montant_paye  
        self.montant_gnf = int(re.sub(r'\s', '', self.montant_gnf))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "base_colis"
        abstract=True
        ordering=['-id']




class Coli(BaseColis):
    class Meta:
        db_table = "colis"

    # def delete(self, *args, **kwargs):
    #     if not isinstance(self, SafeDeleteColis):
    #         SafeDeleteColis.objects.create(
    #             **{field.name: getattr(self, field.name) for field in self._meta.fields if field.name != 'id'}
    #         )
    #     super().delete(*args, **kwargs)


class SafeDeleteColis(BaseColis):
    class Meta:
        db_table="safe_delete_colis_vol"


class CodeColis(models.Model):
    class Meta:
        db_table = "codecolis"

#------------------------BATEAU------------------------------
        
class ColiBateau(models.Model):
    code = models.CharField(max_length=255, verbose_name="Code",unique=True,error_messages={"unique":"Ce code existe déjà, valider à nouveau"})
    montant=models.DecimalField(max_digits=19, decimal_places=2)
    montant_euro=models.DecimalField(max_digits=19, decimal_places=2,null=True,blank=True)
    agence_depart=models.ForeignKey(Agence,on_delete=models.SET_NULL,related_name="agenceb1",null=True,blank=True)
    agence_arrive=models.ForeignKey(Agence,on_delete=models.SET_NULL,related_name="agenceb2",null=True,blank=True)
    expditaire=models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=False,related_name="Expeditaireb")
    destinataire=models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=False,related_name="Destinataireb")
    montant_paye=models.DecimalField(max_digits=19, decimal_places=2,verbose_name="Montant payé",null=True,blank=True)
    reste=models.DecimalField(max_digits=19, decimal_places=2,verbose_name="Reste",null=True,blank=True)
    devise_montantpaye=models.CharField(verbose_name="Dévise",max_length=100,choices=DEVISE)
    devise=models.CharField(max_length=100,default="€",editable=False)
    dates=models.DateField(verbose_name="Date",null=True,blank=True)
    heure=models.DateTimeField(auto_now_add=True)
    montant_euro=models.CharField(max_length=100, verbose_name="Montant en Euro",null=True,blank=True)
    frais=models.DecimalField(max_digits=19, decimal_places=2,null=True,blank=True,verbose_name="Frais de livraison")
    montant_gnf=models.CharField(max_length=100, verbose_name="Montant en GNF",null=True,blank=True)
    conteneurs=models.ForeignKey(Conteneur,on_delete=models.SET_NULL,null=True,blank=False)
    total_paye=models.CharField(max_length=100, verbose_name="Total paye",null=True,blank=True)
    # -------------------------ENREGISTREMEMT----------------------------
    etat_enregistrement=models.CharField(max_length=10,default=1)
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=False)
    date_enregistrement=models.DateField(null=True,blank=True)
    heure_enregistrement=models.DateTimeField(null=True,blank=True)
    # -------------------------MISE EN LOT----------------------------
    etat_lot=models.CharField(max_length=10,default=0)
    user_lot=models.ForeignKey(User,related_name="userb2",on_delete=models.SET_NULL,null=True,blank=True)
    date_lot=models.DateField(null=True,blank=True)
    heure_lot=models.DateTimeField(null=True,blank=True)
    # -------------------------EMBARQUEMENT----------------------------
    etat_embarquement=models.CharField(max_length=10,default=0)
    user_embarquement=models.ForeignKey(User,related_name="userb3",on_delete=models.SET_NULL,null=True,blank=True)
    date_embarquement=models.DateField(null=True,blank=True)
    heure_embarquement=models.DateTimeField(null=True,blank=True)
    # -------------------------VERIFICATION----------------------------
    etat_verification=models.CharField(max_length=10,default=0)
    user_verification=models.ForeignKey(User,related_name="userb4",on_delete=models.SET_NULL,null=True,blank=True)
    date_verification=models.DateField(null=True,blank=True)
    heure_verification=models.DateTimeField(null=True,blank=True)
    # -------------------------RECEPTION----------------------------
    etat_receptionclient=models.CharField(max_length=10,default=0)
    user_receptionclient=models.ForeignKey(User,related_name="userb5",on_delete=models.SET_NULL,null=True,blank=True)
    date_receptionclient=models.DateField(null=True,blank=True)
    heure_receptionclient=models.DateTimeField(null=True,blank=True)
    montant_reglement=models.IntegerField(verbose_name="Montant",null=True,blank=True)
    devise_reglement=models.CharField(verbose_name="Dévise",max_length=100,choices=DEVISE)
    taux=models.CharField(max_length=100,null=True,blank=True)
    types=models.CharField(max_length=255,null=True,blank=True)
   
    def save(self, *args, **kwargs):     
        if self.montant_paye==None:
            montant_paye=0
        else:
            montant_paye=str(float(self.montant_paye)).replace(" ","")
        self.montant_paye=montant_paye    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "colis_bateau"
        ordering=['-id']
    

class CodeColisBateau(models.Model):
    conteneurs=models.ForeignKey(Conteneur,on_delete=models.SET_NULL,null=True,blank=False)
    class Meta:
        db_table = "codecolis_bateau"


    
class DetaiColis(models.Model):
    colis=models.ForeignKey(ColiBateau,on_delete=models.CASCADE,null=True,blank=True)
    designation=models.CharField(max_length=255,verbose_name='Désignation')
    quantite_detail=models.PositiveBigIntegerField(verbose_name='Quantité')
    prix_unitaire = models.DecimalField(verbose_name="Prix unitaire en Euro",max_digits=19, decimal_places=2,validators=[MinValueValidator(0)])
    montant = models.DecimalField(verbose_name="Montant",max_digits=19, decimal_places=2,validators=[MinValueValidator(0)])
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)

    def save(self, *args, **kwargs):         
        self.montant=self.quantite_detail*self.prix_unitaire    
        super().save(*args, **kwargs)

    class Meta:
        db_table = "detail_colis"



class Attribution(models.Model):
    expditaire=models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=False,related_name="Expeditaire1")
    destinataire=models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=False,related_name="Destinataire1")
    class Meta:
        db_table = "attributions"
    


    


# class SafeDeleteColis(Coli):
#     class Meta:
#         db_table="safe_delete_colis_vol"