from django import forms
from .models import Clientsrendezvou

class ClientsrendezvouForm(forms.ModelForm):
	class Meta:
		model=Clientsrendezvou
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})		}
