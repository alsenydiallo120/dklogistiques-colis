from django import forms
from .models import Transporteur

class TransporteurForm(forms.ModelForm):
	class Meta:
		model=Transporteur
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})		}
