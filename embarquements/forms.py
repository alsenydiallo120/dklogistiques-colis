from django import forms
from .models import Embarquement
from transporteurs.models import Transporteur
from agences.models import Agence

class EmbarquementForm(forms.ModelForm):
	class Meta:
		model=Embarquement
		fields='__all__'

		widgets={
			'transporteurs':forms.Select(attrs={
				'class':'form-select',
				'required':'true',
			}),
			'devise':forms.Select(attrs={
				'class':'form-select',
				'required':'true',
			}),
			'agence_arrive':forms.Select(attrs={
				'class':'form-select',
				'required':'true',
			})
		}


class EmbarquementEditForm(forms.ModelForm):
	class Meta:
		model=Embarquement
		fields=['transporteurs','agence_arrive']

		widgets={
			'transporteurs':forms.Select(attrs={
				'class':'form-select',
				'required':'true',
			}),
			
			'agence_arrive':forms.Select(attrs={
				'class':'form-select',
				'required':'true',
			})
		}





class TransportForm(forms.ModelForm):
	class Meta:
		model=Transporteur
		fields=['nom','telephone']

