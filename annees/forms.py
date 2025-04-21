from django import forms
from .models import Annee

class AnneeForm(forms.ModelForm):
	class Meta:
		model=Annee
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})		}
