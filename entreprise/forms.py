from django import forms
from .models import Entreprise

class EntrepriseForm(forms.ModelForm):
    class Meta:
      model=Entreprise
      fields='__all__'
      widgets = {
            'header_color': forms.TextInput(attrs={
              'type': "color"
              }
            ),
            'header_color_left': forms.TextInput(attrs={
              'type': "color"
              }
            ),
        }
