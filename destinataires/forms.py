from django import forms
from .models import Destinataire

class DestinataireForm(forms.ModelForm):
	class Meta:
		model=Destinataire
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})		}
