from django import forms
from .models import Conteneur
from django.core.exceptions import NON_FIELD_ERRORS




class ConteneurForm(forms.ModelForm):
	class Meta:
		model=Conteneur
		exclude=["libelle"]

		widgets={
			'dates':forms.DateInput(attrs={
				'type':'date'
			}),
			
		}

		error_messages = {
			NON_FIELD_ERRORS: {
				'unique_together': 'Ce code de conteneur existe déjà',
			}
		}


class ClotureConteneurForm(forms.ModelForm):
	class Meta:
		model=Conteneur
		fields=["id"]