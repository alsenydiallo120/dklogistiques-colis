from django import forms
from .models import Typecompte

class TypecompteForm(forms.ModelForm):
	class Meta:
		model=Typecompte
		exclude = ('statut',)

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			}),
			'libelle': forms.TextInput(attrs={'required':True})}