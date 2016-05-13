from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,Http404, HttpResponseRedirect

from login.views import *

from establishments.forms import *
from establishments.models import *
#from establishments.views import *

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

def edit_restaurant(request, establishment_id):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = RestaurantForm(request.POST)
		if form.is_valid():
			success = Restaurant.db.edit_from_dict(form.cleaned_data, establishment_id)
			if success :
				return redirect("/establishments/restaurant/"+str(establishment_id))
		form.add_error(None, "error")
		context["form"] = form
		context["establishment_id"] = establishment_id
		return render(request, 'admin/edit_restaurant.html', context)
	else:
		restaurant = Restaurant.db.get_by_id(establishment_id)
		if restaurant == None :
			raise Http404("Restaurant does not exit")
		context["establishment_id"] = establishment_id
		db_dict = restaurant.get_dict()
		
		form = RestaurantForm()
		for field in form.fields:
			form.initial[field] = db_dict[field]
		context["form"] = form
		return render(request, 'admin/edit_restaurant.html', context)

def edit_bar(request, establishment_id):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = BarForm(request.POST)
		if form.is_valid():
			success = Bar.db.edit_from_dict(form.cleaned_data, establishment_id)
			if success :
				return redirect("/establishments/bar/"+str(establishment_id))
		form.add_error(None, "error")
		context["form"] = form
		context["establishment_id"] = establishment_id
		return render(request, 'admin/edit_bar.html', context)
	else:
		bar = Bar.db.get_by_id(establishment_id)
		if bar == None :
			raise Http404("Bar does not exit")
		context["establishment_id"] = establishment_id
		db_dict = bar.get_dict()
		
		form = BarForm()
		for field in form.fields:
			form.initial[field] = db_dict[field]
		context["form"] = form
		return render(request, 'admin/edit_bar.html', context)

def edit_hotel(request, establishment_id):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = HotelForm(request.POST)
		if form.is_valid():
			success = Hotel.db.edit_from_dict(form.cleaned_data, establishment_id)
			if success :
				return redirect("/establishments/hotel/"+str(establishment_id))
		form.add_error(None, "error")
		context["form"] = form
		context["establishment_id"] = establishment_id
		return render(request, 'admin/edit_hotel.html', context)
	else:
		hotel = Hotel.db.get_by_id(establishment_id)
		if hotel == None :
			raise Http404("Hotel does not exit")
		context["establishment_id"] = establishment_id
		db_dict = hotel.get_dict()
		
		form = HotelForm()
		for field in form.fields:
			form.initial[field] = db_dict[field]
		context["form"] = form
		return render(request, 'admin/edit_hotel.html', context)

def delete_restaurant(request, establishment_id):
	(context, user, res) = check_admin(request)
	if res : return res
	success = Restaurant.db.delete(establishment_id)
	if success :
		return redirect('establishments.views.index')
	else:
		return redirect("/establishments/restaurant/"+str(establishment_id))

def delete_bar(request, establishment_id):
	(context, user, res) = check_admin(request)
	if res : return res
	success = Bar.db.delete(establishment_id)
	if success :
		return redirect('establishments.views.index')
	else:
		return redirect("/establishments/bar/"+str(establishment_id))

def delete_hotel(request, establishment_id):
	(context, user, res) = check_admin(request)
	if res : return res
	success = Hotel.db.delete(establishment_id)
	if success :
		return redirect('establishments.views.index')
	else:
		return redirect("/establishments/hotel/"+str(establishment_id))


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

def edit_user(request, username):
	(context, user, res) = check_admin(request)
	if res : return res
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_username = form.cleaned_data['username']
			success = User.db.edit_from_dict(form.cleaned_data, username)
			if success :
				return redirect("/users/"+new_username)
		form.add_error(None, "error")
		context["form"] = form
		context["username"] = username
		context["password"] = form.cleaned_data["password"]
		return render(request, 'admin/edit_user.html', context)
	else:
		searched_user = User.db.get(username)
		if searched_user == None :
			raise Http404("User does not exit")
		db_dict = searched_user.get_dict()
		form = RegisterForm()
		for field in form.fields:
			if field in db_dict :
				form.initial[field] = db_dict[field]
		form.initial["username"] = db_dict["name"]
		context["form"] = form
		context["username"] = username
		context["password"] = searched_user.password
		return render(request, 'admin/edit_user.html', context)


def delete_user(request, username):
	(context, user, res) = check_admin(request)
	if res : return res
	success = User.db.delete(username)
	if success :
		return redirect('users.views.index')
	else:
		return redirect("/users/"+username)


