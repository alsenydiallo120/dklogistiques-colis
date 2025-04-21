from django import forms
from regulationbateaus.models import Regulationbateau
from regulations.models import Regulation
from .models import Reglement
from colis.models import Coli, ColiBateau
from .import my_widgets as customWidget
from django.db.models import Sum



class ReglementForm(forms.ModelForm):
    class Meta:
        model=Reglement
        exclude=("author","agences","updated_at","colisbateau",)

        widgets={
            'dates':forms.DateInput(attrs={
                'type':'date'
            }),
            'reste_euro':forms.DateInput(attrs={
                'readonly':True
            }),
            'reste_gnf':forms.DateInput(attrs={
                'readonly':True
            }),
            'colis':forms.Select(attrs={
                'class':'customselect'
            }),
        }

    # def __init__(self, *args, **kwargs):
    #         agence=kwargs['initial']['agences_id']
    #         colis=Coli.objects.select_related("agence_depart","agence_arrive","expditaire","destinataire").filter(etat_receptionclient=0).exclude(agence_depart_id=agence)
    #         super(ReglementForm, self).__init__(*args, **kwargs)
    #         self.fields['colis'] = forms.ModelChoiceField(
    #             initial=None, queryset=colis,
    #             widget=customWidget.CustomSelect(modify_choices=tuple(
    #                 [(coli.id, 
    #                 coli.expditaire,
    #                 coli.destinataire, 
    #                 coli.montant,
    #                 float(coli.total_paye),
    #                 float(coli.reste)
    #                 ) 
    #                 for coli in colis]
    #             )))

class ReglementFormGuinee(forms.ModelForm):
    class Meta:
        model=Reglement
        exclude=("author","agences","updated_at","colisbateau",)

        widgets={
            'dates':forms.DateInput(attrs={
                'type':'date'
            }),
            'reste_euro':forms.DateInput(attrs={
                'readonly':True
            }),
            'reste_gnf':forms.DateInput(attrs={
                'readonly':True
            }),
            'colis':forms.Select(attrs={
                'class':'customselect'
            }),
        }

    # def __init__(self, *args, **kwargs):
    #         agence=kwargs['initial']['agences_id']
    #         colis=Coli.objects.filter(etat_receptionclient=0).exclude(agence_depart_id=agence)
    #         super(ReglementFormGuinee, self).__init__(*args, **kwargs)
    #         self.fields['colis'] = forms.ModelChoiceField(
    #             initial=None, queryset=colis,
    #             widget=customWidget.CustomSelect(modify_choices=tuple(
    #                 [(coli.id, 
    #                 coli.expditaire,
    #                 coli.destinataire, 
    #                 coli.montant,
    #                 float(coli.total_paye),
    #                 float(coli.reste)
    #                 ) 
    #                 for coli in colis]
    #             )))



class ReglementBateauForm(forms.ModelForm):
    class Meta:
        model=Reglement
        exclude=("author","agences","updated_at","colis",)

        widgets={
            'dates':forms.DateInput(attrs={
                'type':'date'
            }),
            'reste_euro':forms.DateInput(attrs={
                'readonly':True
            }),
            'reste_gnf':forms.DateInput(attrs={
                'readonly':True
            }),
            'colisbateau':forms.Select(attrs={
                'class':'customselect'
            }),
           
        }

    def __init__(self, *args, **kwargs):
            colis=ColiBateau.objects.select_related("agence_depart","agence_arrive","expditaire","destinataire").filter(etat_receptionclient=0)
            super(ReglementBateauForm, self).__init__(*args, **kwargs)
            self.fields['colisbateau'] = forms.ModelChoiceField(
                initial=None, queryset=colis,
                widget=customWidget.CustomSelect(modify_choices=tuple(
                    [(coli.id, 
                    coli.expditaire,
                    coli.destinataire, 
                    coli.montant,
                    float(coli.total_paye),
                    float(coli.reste)
                    ) 
                    for coli in colis]
                )))