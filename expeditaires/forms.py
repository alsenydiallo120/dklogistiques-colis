from django import forms
from .models import Expeditaire

class ExpeditaireForm(forms.ModelForm):
	class Meta:
		model=Expeditaire
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})
		}
