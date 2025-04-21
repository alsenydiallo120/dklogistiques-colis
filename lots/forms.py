from django import forms
from .models import Lot

class LotForm(forms.ModelForm):
	class Meta:
		model=Lot
		fields='__all__'

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			})}
