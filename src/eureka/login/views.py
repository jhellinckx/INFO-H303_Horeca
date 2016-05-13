from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from login.models import *

from .forms import *

def _login(request, user):
	request.session["user"] = user

def login(request):
	if(request.session.has_key("user")):
		return HttpResponse("Already logged in")
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid() :
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = User.db.get(username, password)
			if user == None :
				form.add_error(None, "error")
				context = {"form" : form}
				return render(request, 'login/login.html', context)			
			else :
				_login(request, user)
				return redirect("establishments.views.index")
	else :
		context	= {"form" : LoginForm()}
		return render(request, 'login/login.html', context)

def register(request):
	if request.method == 'POST':
		return HttpResponse("TODO")
	else :
		return HttpResponse("TODO")