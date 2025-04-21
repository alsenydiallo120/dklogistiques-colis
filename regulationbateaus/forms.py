from django import forms
from .models import *
from .import my_widgets as customWidget
from colis.models import ColiBateau
from django.db.models import Sum




class RegulationbateauForm(forms.ModelForm):
    class Meta:
        model=Regulationbateau
        fields='__all__'

        widgets={
            'dates':forms.DateInput(attrs={
                'type':'date'
            }),
            'colis':forms.Select(attrs={
                'class':'customselect'
            }),
        }

    # def __init__(self, *args, **kwargs):
    #     pays=kwargs['initial']['pays']
    #     colis=ColiBateau.objects.filter(etat_receptionclient=0,agence_depart__pays_id=pays)
    #     super(RegulationbateauForm, self).__init__(*args, **kwargs)
    #     self.fields['colis'] = forms.ModelChoiceField(
    #         initial=None, queryset=colis,
    #         widget=customWidget.CustomSelect(modify_choices=tuple(
    #             [(coli.id, 
    #               coli.expditaire,
    #               coli.destinataire, 
    #               coli.montant or 0,
    #               float(coli.montant_paye or 0)+float((Regulationbateau.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0)),
    #               float(coli.montant or 0)-float(coli.montant_paye or 0)-float((Regulationbateau.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
    #               ) 
    #              for coli in colis]
    #         )))
