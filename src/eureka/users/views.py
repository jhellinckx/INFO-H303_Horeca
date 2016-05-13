from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.db import connection

from login.views import *
from login.models import *
from establishments.models import *
from tags.models import *
from common.models import BaseDBManager

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
	getUserEstablishmentComments(context, username)
	getUserTags(context, username)
	return render(request, 'users/user_detail.html', context)


def getUserEstablishmentComments(context, username):
	restaurants_list, bars_list, hotels_list = [],[],[]
	with connection.cursor() as c:
		manager = BaseDBManager()
		c.execute('SELECT * FROM "Restaurant" JOIN "Establishment" ON "Restaurant".establishment_id = "Establishment".id WHERE establishment_id IN (SELECT establishment_id FROM "EstablishmentComment" WHERE user_name = %s);', [username])
		restaurants_list = [Restaurant.from_db(d) for d in manager.fetch_dicts(c)]
		c.execute('SELECT * FROM "Bar" JOIN "Establishment" ON "Bar".establishment_id = "Establishment".id WHERE establishment_id IN (SELECT establishment_id FROM "EstablishmentComment" WHERE user_name = %s);', [username])
		bars_list = [Bar.from_db(d) for d in manager.fetch_dicts(c)]
		c.execute('SELECT * FROM "Hotel" JOIN "Establishment" ON "Hotel".establishment_id = "Establishment".id WHERE establishment_id IN (SELECT establishment_id FROM "EstablishmentComment" WHERE user_name = %s);', [username])
		hotels_list = [Hotel.from_db(d) for d in manager.fetch_dicts(c)]
	if len(restaurants_list) != 0:
		context['restaurants_list'] = restaurants_list
	if len(bars_list) != 0:
		context['bars_list'] = bars_list
	if len(hotels_list) != 0:
		context['hotels_list'] = hotels_list

def getUserTags(context, username):
	tags_list = []
	with connection.cursor() as c:
		manager = BaseDBManager()
		c.execute('SELECT DISTINCT t.name FROM "Tag" t, "EstablishmentTags" et WHERE t.name = et.tag_name AND et.user_name = %s', [username])
		tags_list = [Tag.from_db(d) for d in manager.fetch_dicts(c)]
	if len(tags_list) != 0:
		context['tags_list'] = tags_list
