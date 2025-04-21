from django import forms
from .models import *
from conteneurs.models import Conteneur
from datetime import date


class DepenseVolForm(forms.ModelForm):
	class Meta:
		model=Depensevol
		exclude=("author","agences","devise",)

		widgets={
			'dates':forms.TextInput(attrs={
				'type':'date',
			}),
			'conteneurs':forms.Select(attrs={
				'class':'customselect',
			}),
			
		}
	

