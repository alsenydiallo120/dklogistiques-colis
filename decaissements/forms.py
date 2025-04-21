from django import forms
from .models import Decaissement
from accounts.models import CustomUser


class DecaissementForm(forms.ModelForm):
    class Meta:
        model=Decaissement
        exclude=["agences","etat","emetteur","validate_by"]
        widgets={
            'dates':forms.TextInput(attrs={
                'type':'date'
            })
        }
    def __init__(self, *args, **kwargs):
        super(DecaissementForm, self).__init__(*args, **kwargs)
        user=kwargs['initial']['user']
        self.fields['recepteur'].queryset = CustomUser.objects.exclude(id=user)
       


class ValideForm(forms.ModelForm):
    class Meta:
        model=Decaissement
        fields=["etat"]
        widgets={
            'etat':forms.CheckboxInput(attrs={
                'hidden':True
            })
        }

    
