from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from login.models import *

from .forms import *

def _login(request, user):
	request.session["username"] = user.name

def _logout(request):
	request.session["username"] = None

def get_user(request):
	user = None
	if request.session.has_key("username"):
		user = User.db.get(request.session["username"])
	return user

def user_context(request):
	return {"user" : get_user(request)}

def login(request):
	context = user_context(request)
	user = context["user"]
	if user != None:
		return HttpResponse("Already logged in")
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid() :
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = User.db.get_with_password(username, password)
			if user == None :
				form.add_error(None, "error")
				context["form"] = form
				return render(request, 'login/login.html', context)			
			else :
				_login(request, user)
				return redirect("establishments.views.index")
		else:
			form.add_error(None, "error")
			context["form"] = form
			return render(request, 'login/login.html', context)		
	else :
		context["form"] = LoginForm()
		return render(request, 'login/login.html', context)

def register(request):
	context = user_context(request)
	user = context["user"]
	if user != None:
		return HttpResponse("Already logged in")
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			success = User.db.create_user(username, email, password, False)	
			if success:
				return redirect("login.views.login")
		form.add_error(None, "error")
		context["form"] = form
		return render(request, 'login/register.html', context)
	else :
		context["form"] = RegisterForm()
		return render(request, 'login/register.html', context)

def logout(request):
	user = get_user(request)
	if user == None:
		return HttpResponse("Not logged in")
	_logout(request)
	return redirect("login.views.login")
