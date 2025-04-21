from django import forms
from .models import Rendezvou
from clientsrendezvous.models import Clientsrendezvou
from .import my_widgets as customWidget
from chauffeurs.models import Chauffeur



class CForm(forms.Form):  
    chauffeurs = forms.ModelChoiceField(
        label='', 
        required=True,
        queryset=Chauffeur.objects.all(),
        empty_label="Selectionner le Chauffeur",
		widget=forms.Select(attrs={'class': 'select2'})
    )


class RendezvouForm(forms.ModelForm):
	class Meta:
		model=Rendezvou
		fields='__all__'
		widgets={
			'dates':forms.TextInput(attrs={
				'type':'date'
			}),
			'heure_debut':forms.TextInput(attrs={
				'type':'time'
			}),
			'heure_fin':forms.TextInput(attrs={
				'type':'time'
			})
		}

	def __init__(self, *args, **kwargs):
			clients= Clientsrendezvou.objects.all()
			super(RendezvouForm, self).__init__(*args, **kwargs)
			self.fields['clients'] = forms.ModelChoiceField(
				initial=None, queryset=clients,
				widget=customWidget.CustomSelect(modify_choices=tuple(
					[(coli.id, 
					coli.telephone or "",
					coli.adresse or "", 
					coli.rue or "",
					coli.code_postal or "",
					coli.ville or "",
					coli.etage or "",
					coli.code or "",
					coli.num_app or "",
					coli.ascenseur or ""
					) 
					for coli in clients]
				)))