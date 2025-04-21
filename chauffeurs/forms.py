from django import forms
from .models import Chauffeur

class ChauffeurForm(forms.ModelForm):
	class Meta:
		model=Chauffeur
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})
		}
