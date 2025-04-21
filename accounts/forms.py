from dataclasses import fields
from pyexpat import model
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['nom','telephone','email','agences','username','agences','types','password1','password2']
        
class RegisterEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['nom','telephone','email','agences','types','username']
     

class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'type':'number'}),label='Téléphone')
    password = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'type':'password'}))



class updatePasswordForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username',"password1"]

        widgets={
			'username':forms.TextInput(attrs={
				'readonly':True,
			}),
		}
        