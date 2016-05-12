from django.shortcuts import render
from django.http import HttpResponse
from .forms import *

def login(request):
	if request.method == 'POST':
		print form.cleaned_data['username']
		print form.cleaned_data['password']
	else:
		form = LoginForm()


	return HttpResponse("salut")

def register(request):
	if request.method == 'POST':
		return HttpResponse("TODO")
	else :
		form = RegisterForm()