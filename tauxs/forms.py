from django import forms
from .models import Taux

class TauxForm(forms.ModelForm):
	class Meta:
		model=Taux
		exclude=["author"]

		widgets={
			'euro':forms.DateInput(attrs={
				'readonly':True
			})
		}
