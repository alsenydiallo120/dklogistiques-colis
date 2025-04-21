from django import forms
from .models import Depense
from conteneurs.models import Conteneur
from datetime import date


class DepenseForm(forms.ModelForm):
	class Meta:
		model=Depense
		exclude=("author","agences","devise",)

		widgets={
			'dates':forms.TextInput(attrs={
				'type':'date',
			}),
			'conteneurs':forms.Select(attrs={
				'class':'customselect',
			}),
			
		}
	def __init__(self, *args, **kwargs):
		super(DepenseForm, self).__init__(*args, **kwargs)
		self.fields['conteneurs'].queryset = Conteneur.objects.all().order_by("-id")
		# if role==False:
		# 	if typeuser=="Bateau":
		# 		self.fields['types'].initial = 'Bateau'
		# 		self.fields['dates'].initial = date.today()
		# 		self.fields['dates'].widget.attrs['readonly'] = True
		# 		self.fields['conteneurs'].initial = Conteneur.objects.filter(cloture=0).last()
		# 	elif typeuser=="Vol":
		# 		self.fields['types'].initial = 'Vol'
		# 		self.fields['dates'].initial = date.today()
		# 		self.fields['dates'].widget.attrs['readonly'] = True
		# else:
		# 	pass


