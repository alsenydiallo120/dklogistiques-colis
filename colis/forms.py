from django import forms
from clients.models import Client
from .models import *
from tauxs.models import Taux
from .import my_widgets as customWidget




class ColiForm(forms.ModelForm):
    class Meta:
        model=Coli
        fields=[
            'code',
            'poids',
            'prix',
            'devise',
            'nombre_colis',
            'montant_paye',
            'devise_montantpaye',
            'contenu',
            'dates',
            'montant_euro',
            'montant_gnf',
            'taux'
        ]
        widgets={
            'code':forms.TextInput(attrs={
                'readonly':True
            }),
            'montant_euro':forms.TextInput(attrs={
                'readonly':True
            }),
            'montant_gnf':forms.TextInput(attrs={
                'readonly':True
            }),
        }

    def __init__(self, *args, **kwargs):
        pays=kwargs['initial']['pays']
        super(ColiForm, self).__init__(*args, **kwargs)
        devise=""
        taux=""
        if pays is not None:
            devise="€"
            taux=Taux.objects.first().gnf
        self.fields['devise'].initial=devise
        self.fields['taux'].initial=taux

       


class EditColiForm(forms.ModelForm):
    class Meta:
        model=Coli
        fields=[
            'code',
            'poids',
            'prix',
            'devise',
            'nombre_colis',
            'expditaire',
            'destinataire',
            'montant_paye',
            'devise_montantpaye',
            'contenu',
            'montant_euro',
            'montant_gnf',
            'taux'
            ]

        widgets={
            'code':forms.TextInput(attrs={
                'readonly':True
            }),
            'montant_euro':forms.TextInput(attrs={
                'readonly':True
            }),
            'montant_gnf':forms.TextInput(attrs={
                'readonly':True
            }),
            'destinataire':forms.Select(attrs={
                'class':"customselect"
            }),
            'expditaire':forms.Select(attrs={
                'class':"customselect"
            }),
        }

 

class RapportForm(forms.ModelForm):
    class Meta:
        model=Coli
        fields=['dates']
        widgets={
            'dates':forms.DateInput(attrs={
                'type':'date'
            }),
        }




class ColiBateauForm(forms.ModelForm):
    class Meta:
        model=ColiBateau
        fields=[
            'code',
            'expditaire',
            'destinataire',
            'montant_paye',
            'devise_montantpaye',
            'dates',
            'montant_euro',
            'montant_gnf',
            'taux',
            'conteneurs',
            'frais'
        ]

        widgets={
           
            'code':forms.TextInput(attrs={
                'readonly':True
            }),
            'montant_euro':forms.TextInput(attrs={
                'readonly':True
            }),
            'montant_gnf':forms.TextInput(attrs={
                'readonly':True
            }),
            'destinataire':forms.Select(attrs={
                'class':"customselect"
            }),
            'expditaire':forms.Select(attrs={
                'class':"customselect"
            }),
        }

    def __init__(self, *args, **kwargs):
        slug=kwargs['initial']['slug']
        id_destinataire=kwargs['initial']['id_destinataire']
        super(ColiBateauForm, self).__init__(*args, **kwargs)
        self.fields['expditaire'].queryset = Client.objects.filter(slug=slug)
        clients = Client.objects.filter(id__in=id_destinataire)
        self.fields['destinataire'] = forms.ModelChoiceField(
            initial=None, queryset=clients,
            widget=customWidget.CustomSelect(modify_choices=tuple(clients.values_list('id','nom','telephone','email'))))





class ColiDetailForm(forms.ModelForm):
    class Meta:
        model=DetaiColis
        exclude=['montant']





TYPE = (
	('Imprimer pour les transitaires', 'Imprimer pour les transitaires'),
    ('Imprimer avec la liste des clients', 'Imprimer avec la liste des clients'),
)


class ConteneurPrintForm(forms.Form):

    conteneurs = forms.ModelChoiceField(
        label='Selectionner le conteneur', 
        required=True,
        queryset=Conteneur.objects.all(),
        widget=forms.Select(attrs={
            'class':"customselect"
        })
    )

    type = forms.ChoiceField(
        label="Type de d'impression",
        choices=TYPE,
        required=True,
        widget=forms.Select(attrs={'type': 'select','class':"customselect"})
        
    )
