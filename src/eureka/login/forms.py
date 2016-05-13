from django import forms

from .models import *

class LoginForm(forms.Form):
	username = forms.CharField(max_length=16, label="Username")
	password = forms.CharField(widget=forms.PasswordInput(), max_length=128, label="Password")


class RegisterForm(forms.Form):
	username = forms.CharField(max_length=16, label="Username")
	password = forms.CharField(widget=forms.PasswordInput(), max_length=128, label="Password")
	email = forms.EmailField(max_length=254, label="Email")