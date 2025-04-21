from django import forms
from .models import Regulation
from .import my_widgets as customWidget
from colis.models import Coli
from django.db.models import Sum




class RegulationForm(forms.ModelForm):
    class Meta:
        model=Regulation
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
    #     pays = kwargs['initial']['pays']
    #     # Filtrer les colis
    #     colis = Coli.objects.filter(etat_receptionclient=0, agence_depart__pays_id=pays)
        
    #     # Calculer les montants agrégés pour chaque colis
    #     montant_agreges = Regulation.objects.values('colis_id').annotate(
    #         montant_total=Sum('montant')
    #     ).values('colis_id', 'montant_total')

    #     # Convertir en dictionnaire pour un accès rapide
    #     montant_agreges_dict = {item['colis_id']: item['montant_total'] or 0 for item in montant_agreges}

    #     # Préparer les choix du widget
    #     choices = [
    #         (
    #             coli.id,
    #             coli.expditaire,
    #             coli.destinataire,
    #             coli.montant,
    #             float(coli.montant_paye) + float(montant_agreges_dict.get(coli.id, 0)),
    #             float(coli.montant) - float(coli.montant_paye) - float(montant_agreges_dict.get(coli.id, 0))
    #         ) 
    #         for coli in colis
    #     ]

    #     # Passer les choix au widget
    #     super(RegulationForm, self).__init__(*args, **kwargs)
    #     self.fields['colis'] = forms.ModelChoiceField(
    #         initial=None, queryset=colis,
    #         widget=customWidget.CustomSelect(modify_choices=tuple(choices))
    #     )




    # def __init__(self, *args, **kwargs):
    #     pays=kwargs['initial']['pays']
    #     colis=Coli.objects.filter(etat_receptionclient=0,agence_depart__pays_id=pays)
    #     super(RegulationForm, self).__init__(*args, **kwargs)
    #     self.fields['colis'] = forms.ModelChoiceField(
    #         initial=None, queryset=colis,
    #         widget=customWidget.CustomSelect(modify_choices=tuple(
    #             [(coli.id, 
    #               coli.expditaire,
    #               coli.destinataire, 
    #               coli.montant,
    #               float(coli.montant_paye)+float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0)),
    #               float(coli.montant)-float(coli.montant_paye)-float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
    #               ) 
    #              for coli in colis]
    #         )))
