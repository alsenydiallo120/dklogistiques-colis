from django import forms
from .models import Agence

class AgenceForm(forms.ModelForm):
	class Meta:
		model=Agence
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})
		}
