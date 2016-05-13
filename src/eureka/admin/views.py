from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,Http404, HttpResponseRedirect

from login.views import *

from establishments.forms import *
from establishments.models import *
from establishments.views import *

from login.forms import *
from login.models import *

def check_admin(request):
	context = user_context(request)
	user = context["user"]
	res = None
	if user == None :
		res = redirect('login.views.login')
	elif not user.is_admin :
		res = HttpResponse('You must be an admin to view this page.')
	return (context, user, res)
		

def index(request):
	(context, user, res) = check_admin(request)
	if res : return res
	return render(request, 'admin/index.html', context)

def create_restaurant(request):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = RestaurantForm(request.POST)
		print form.errors
		if form.is_valid():
			(success, establishment_id) = Restaurant.db.create_from_dict(form.cleaned_data, user.name)
			if success :
				return redirect("/establishments/restaurant/"+str(establishment_id))
		form.add_error(None, "error")
		context["form"] = form
		return render(request, 'admin/create_restaurant.html', context)
	else:
		context["form"] = RestaurantForm()
		return render(request, 'admin/create_restaurant.html', context)

def create_bar(request):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = BarForm(request.POST)
		if form.is_valid():
			(success, establishment_id) = Bar.db.create_from_dict(form.cleaned_data, user.name)
			if success :
				return redirect("/establishments/bar/"+str(establishment_id))
		form.add_error(None, "error")
		context["form"] = form
		return render(request, 'admin/create_bar.html', context)
	else:
		context["form"] = BarForm()
		return render(request, 'admin/create_bar.html', context)

def create_hotel(request):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = HotelForm(request.POST)
		if form.is_valid():
			(success, establishment_id) = Hotel.db.create_from_dict(form.cleaned_data, user.name)
			if success :
				return redirect("/establishments/hotel/"+str(establishment_id))
		form.add_error(None, "error")
		context["form"] = form
		return render(request, 'admin/create_hotel.html', context)
	else:
		context["form"] = HotelForm()
		return render(request, 'admin/create_hotel.html', context)

def create_user(request):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			is_admin = form.cleaned_data['is_admin']
			success = User.db.create_user(username, email, password, is_admin)	
			if success :
				return HttpResponse("CREATION SUCCESSFUL : TODO : DISPLAY USER")
		form.add_error(None, "error")
		context["form"] = form
		return render(request, 'admin/create_user.html', context)
	else:
		context['form'] = RegisterForm()
		return render(request, 'admin/create_user.html', context)

