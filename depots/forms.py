from django import forms
from .models import Depot

class DepotForm(forms.ModelForm):
	class Meta:
		model=Depot
		exclude=('author','agences',)

		widgets={
			'dates':forms.TextInput(attrs={
				'type':'date',
				'readonly':True
			}),
			'montant':forms.TextInput(attrs={
				'class':'champ'
			}),
		}
