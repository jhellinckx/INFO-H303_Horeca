from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,Http404, HttpResponseRedirect

from login.views import *

def index(request):
	context = user_context(request)
	user = context["user"]
	if user == None :
		return redirect('login.views.login')
	elif not user.is_admin :
		return HttpResponse('You must be an admin to view this page.')
	else:
		return render(request, 'admin/index.html', context)

def create_restaurant(request):
	return HttpResponse('resto')

def create_bar(request):
	return HttpResponse('bar')

def create_hotel(request):
	return HttpResponse('hotel')

def create_user(request):
	return HttpResponse('user')

