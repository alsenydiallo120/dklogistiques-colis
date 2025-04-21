from django import forms
from accounts.models import CustomUser
from agences.models import Agence


Types = (
	('', "Selectionner le type d'envoi"),
	('Vol', 'Vol'),
    ('Bateau', 'Bateau'),
)

class RapportForm(forms.Form):
    date_debut = forms.DateField(
        label='Date début', 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_fin = forms.DateField(
        label='Date fin', 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    agences = forms.ModelChoiceField(
        label='Agence', 
        required=True,
        queryset=Agence.objects.all(),
        empty_label="Toutes les agences"
    )
    agent = forms.ModelChoiceField(
        label='Utilisateur', 
        required=False,
        queryset=CustomUser.objects.all(),
        empty_label="Tous les utilisateurs"
    )
    types = forms.ChoiceField(
        label='Type',
        required=True,
        choices=Types,
        widget=forms.Select()
    )
