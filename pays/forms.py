from django import forms
from .models import Pay

class PayForm(forms.ModelForm):
	class Meta:
		model=Pay
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})		}
