# forms.py
from django import forms

class LoginForm(forms.Form):
    telephone = forms.CharField(label="Numéro de téléphone", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
