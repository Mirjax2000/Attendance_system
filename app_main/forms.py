from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Uživatelské jméno', max_length=254)
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput)