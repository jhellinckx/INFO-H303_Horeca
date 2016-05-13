from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect

from login.views import *
from login.models import *

def index(request):
	context = user_context(request)
	user = context["user"]
	context["all_users_list"] = User.db.get_all()
	return render(request, 'users/index.html', context)

def user_detail(request, username):
	context = user_context(request)
	user = context["user"]
	searched_user = User.db.get(username)
	if searched_user == None :
		raise Http404("Username does not exist")
	context["searched_user"] = searched_user
	return render(request, 'users/user_detail.html', context)