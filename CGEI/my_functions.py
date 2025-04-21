
from decimal import Decimal
from django.db.models import Sum
from datetime import datetime
import secrets
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import requests
from django.urls import path
from django.contrib.auth.decorators import login_required
from datetime import date
from colis.models import Coli, ColiBateau
from decaissements.models import Decaissement
from depenses.models import Depense
from depensevols.models import Depensevol
from reglements.models import Reglement
from regulationbateaus.models import Regulationbateau
from regulations.models import Regulation
from django.db.models import Q
from django.db import transaction




def convert_date_courte(date):
    dates=datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    return dates



def caisse_paris(utilisateur):
    datej="2024-04-20"
    colis_bateau=ColiBateau.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    colis_vol=Coli.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    reglements=Regulation.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    reglements_bateau=Regulationbateau.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    receptions=Reglement.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    depense_bateau=Depense.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    depense_vol=Depensevol.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    decaissement=Decaissement.objects.filter(Q(dates__gte=datej),emetteur_id=utilisateur,etat=True)
    #-------------------------------SOMMATION--------------------------------
    montant_colis_bateau=colis_bateau.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0
    montant_colis_vol=colis_vol.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0
    montant_reglements=reglements.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_reglements_bateau=reglements_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_receptions=receptions.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
    montant_depense_bateau=depense_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_depense_vol=depense_vol.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_decaissement=decaissement.aggregate(Sum("montant"))["montant__sum"] or 0
    caisse_paris=Decimal(montant_colis_bateau)+Decimal(montant_colis_vol)+Decimal(montant_reglements)+Decimal(montant_reglements_bateau)+Decimal(montant_receptions)-Decimal(montant_depense_bateau)-Decimal(montant_depense_vol)-Decimal(montant_decaissement)
    return caisse_paris



def caisse_guinee(utilisateur,devis):
    datej="2024-06-13"
    #------------------------------REQUETE GNF------------------------------
    colis_vol=Coli.objects.filter(Q(dates__gte=datej,devise_montantpaye=devis),author_id=utilisateur)
    receptions=Reglement.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    depense_bateau=Depense.objects.filter(Q(dates__gte=datej), author_id=utilisateur,devise=devis)
    depense_vol=Depensevol.objects.filter(Q(dates__gte=datej), author_id=utilisateur,devise=devis)
    decaissement=Decaissement.objects.filter(Q(dates__gte=datej),emetteur_id=utilisateur,etat=True,devise=devis)
    encaissement=Decaissement.objects.filter(Q(dates__gte=datej),recepteur_id=utilisateur,etat=True,devise=devis)
    #-------------------------------SOMMATION GNF--------------------------------
    montant_colis_vol=colis_vol.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0
    if devis=="gnf":
        montant_receptions=receptions.aggregate(Sum("montant_gnf"))["montant_gnf__sum"] or 0
    else:
        montant_receptions=receptions.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
    montant_depense_bateau=depense_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_depense_vol=depense_vol.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_encaissement=encaissement.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_decaissement=decaissement.aggregate(Sum("montant"))["montant__sum"] or 0
    caisse_guinee=int(montant_colis_vol)+int(montant_receptions)+int(montant_encaissement)-int(montant_depense_bateau)-int(montant_depense_vol)-int(montant_decaissement)
    # caisse_guinee=int(montant_receptions)
    return caisse_guinee



def caisse_paris_general(utilisateur):
    datej="2024-04-20"
    colis_bateau=ColiBateau.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    colis_vol=Coli.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    reglements=Regulation.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    reglements_bateau=Regulationbateau.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    receptions=Reglement.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    depense_bateau=Depense.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    depense_vol=Depensevol.objects.filter(Q(dates__gte=datej), author_id=utilisateur)
    decaissement=Decaissement.objects.filter(Q(dates__gte=datej),emetteur_id=utilisateur,etat=True)
    #-------------------------------SOMMATION--------------------------------
    montant_colis_bateau=colis_bateau.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0
    montant_colis_vol=colis_vol.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0
    montant_reglements=reglements.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_reglements_bateau=reglements_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_receptions=receptions.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
    montant_depense_bateau=depense_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_depense_vol=depense_vol.aggregate(Sum("montant"))["montant__sum"] or 0
    montant_decaissement=decaissement.aggregate(Sum("montant"))["montant__sum"] or 0
    caisse=Decimal(montant_colis_bateau)+Decimal(montant_colis_vol)+Decimal(montant_reglements)+Decimal(montant_reglements_bateau)+Decimal(montant_receptions)-Decimal(montant_depense_bateau)-Decimal(montant_depense_vol)-Decimal(montant_decaissement)
    return caisse


def caisse_admin_paris(utilisateur):
    datej="2024-04-20"
    decaissement=Decaissement.objects.filter(Q(dates__gte=datej),recepteur_id=utilisateur,etat=True)
    montant=Decimal(decaissement.aggregate(Sum("montant"))["montant__sum"] or 0)
    return montant


def check_invalid_fields(form):
    invalid_fields = [field for field in form if field.errors]
    invalid_field_names = [field.name for field in invalid_fields]  
    invalid_field_values = [field.values() for field in invalid_fields]  
    print("Champs invalides par nom :", invalid_field_names)
    print("Champs invalides par nom :", invalid_field_values)


def convert_date_courte(date):
    dates=datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    return dates


def generate_urlpatterns(app_name, view_class):
    return [
        path('', login_required(view_class.as_view()), name=f'{app_name}-index'),
        path('create/', login_required(view_class.as_view()), name=f'{app_name}-create'),
        path('edit/<int:pk>/', login_required(view_class.as_view()), name=f'{app_name}-edit'),
        path('delete/<int:pk>/', login_required(view_class.as_view()), name=f'{app_name}-delete'),
    ]

def generate_urlpatterns(app_name, view_class, specific_url=''):
    return [
        path(specific_url, login_required(view_class.as_view()), name=f'{app_name}-index'),
        path(f'{specific_url}create/', login_required(view_class.as_view()), name=f'{app_name}-create'),
        path(f'{specific_url}edit/<int:pk>/', login_required(view_class.as_view()), name=f'{app_name}-edit'),
        path(f'{specific_url}delete/<int:pk>/', login_required(view_class.as_view()), name=f'{app_name}-delete'),
    ]


def send_sms(message,phonenumber,username,token,sender):
    mobile_number="224"+phonenumber
    url="https://smswanwaran.com/index.php?app=ws&u="+(username)+"&h="+(token)+"&op=pv&to="+(mobile_number)+"&msg="+(message)+"&from="+(sender)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, headers=headers)
    return r


def calculer_somme(queryset, champ):
    return queryset.aggregate(Sum(champ))[f"{champ}__sum"] or 0



def calcule_reste_vol_paris(colis_id):
    coli=Coli.objects.filter(id=colis_id).first()
    reste=0
    total_paye=0
    data=[]
    if coli is not None:
        reglement=Regulation.objects.filter(colis_id=colis_id)
        total_reglement=reglement.aggregate(Sum("montant"))['montant__sum'] or 0
        if coli.devise_montantpaye=="€":
            total_paye=float(coli.montant_paye)+float(total_reglement)
        else:
            total_paye=float(coli.montant_paye)/float(coli.taux)+float(total_reglement)
        reste=float(coli.montant)-total_paye
    data=[reste,total_paye]
    Coli.objects.filter(id=colis_id).update(total_paye=total_paye,reste=reste)
    return data



def calcule_reste_bateau(colis_id):
    coli=ColiBateau.objects.filter(id=colis_id).first()
    reste=0
    total_paye=0
    data=[]
    if coli is not None:
        regulation_bateau=Regulationbateau.objects.filter(colis_id=colis_id)
        total_reglement=regulation_bateau.aggregate(Sum("montant"))['montant__sum'] or 0
        total_paye=float(coli.montant_paye)+float(total_reglement)
        reste=float(coli.montant)-total_paye
    data=[reste,total_paye]
    ColiBateau.objects.filter(id=colis_id).update(total_paye=total_paye,reste=reste)
    return data



def calcule_reste_bateau_paris(colis_id):
    coli=Coli.objects.filter(id=colis_id).first()
    reste=0
    if coli is not None:
        reste=float(coli.montant)-float(coli.montant_paye)-float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
    return reste


def get_permissions_grouped_by_model(query=""):
    permissions_by_model = {}
    content_types = ContentType.objects.filter(model__icontains=query)
    excludes_models=["contenttype","dontsendentry","group","message","messagelog","session","logentry","permission","groupe"]
    for content_type in content_types:
        permissions = Permission.objects.filter(content_type=content_type).exclude(content_type__model__in=excludes_models)
        if permissions:
            permission_names = [{'id': permission.id, 'name': permission.name.replace("Can","Peut").replace("delete","supprimer un").replace("change","modifier un").replace("add","ajouter un").replace("view","voir un").replace("custom user","utilisateur")} for permission in permissions]
            permissions_by_model[content_type.model] = permission_names
    permissions_grouped = permissions_by_model
    return permissions_grouped


def conversion_chaine(chaine):
    if chaine==None:
        return 0
    elif isinstance(chaine, str):
        if chaine=="":
            chaine="0"
        new_chaien=chaine.replace(",","")
        chaine=int(new_chaien)
        return chaine


def convert_date_courte(date):
    dates=datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    return dates
    

def format_montant(montant):
    montant_formate=f"{int(montant):,}".replace(","," ")
    return montant_formate
    



