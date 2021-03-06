from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.db import connection

from establishments.models import *
from tags.models import *
from comments.models import EstablishmentComment
from login.models import User
from common.models import BaseDBManager

from login.views import *

from tags.forms import *
from establishments.forms import *
from comments.forms import EstablishmentCommentForm
import datetime

def index(request):
	context = user_context(request)
	user = context["user"]
	context["all_restaurants_list"] = Restaurant.db.get_all()
	context["all_bars_list"] = Bar.db.get_all()
	context["all_hotels_list"] = Hotel.db.get_all()
	addSearchForm(request, context)
	return render(request, 'establishments/index.html', context)

def getEstablishmentContext(context, request, establishment_id):
	getTagsContext(context, establishment_id)
	getCommentsContext(context, establishment_id)
	getAverageScoreEstablishmentContext(context, establishment_id)
	addCommentForm(request, context, establishment_id)
	addEstablishmentTagForm(request, context, establishment_id)
	return context

def getCommentsContext(context, establishment_id):
	comments = EstablishmentComment.db.get_by_establishment(establishment_id)
	if(len(comments) != 0):
		context['comments_list'] = comments

def getAverageScoreEstablishmentContext(context, establishment_id):
	averageScore = -1
	with connection.cursor() as cursor:
		cursor.execute('SELECT avg(score) FROM "EstablishmentComment" WHERE establishment_id = %s', [establishment_id])
		row = cursor.fetchone()
		averageScore = row[0]
	if averageScore != -1 and averageScore != None:
		context['average_score'] = "{0:.2f}".format(averageScore)

def getTagsContext(context, establishment_id): #same as getCommentsContext
	tags = EstablishmentTag.db.get_by_establishment(establishment_id)
	unique_tags_names = []
	unique_tags = []
	tags_score = {}
	for tag in tags :
		if tag.tag_name not in unique_tags_names:
			unique_tags.append(tag)
			unique_tags_names.append(tag.tag_name)
			tags_score[tag.tag_name] = 1
		else:
			tags_score[tag.tag_name] += 1
	if(len(unique_tags) != 0):
		context['tags_list'] = unique_tags
		context['tags_score'] = tags_score

def restaurant_detail(request, establishment_id):
	context = user_context(request)
	user = context["user"]
	restaurant = Restaurant.db.get_by_id(establishment_id)
	if restaurant == None : 
		raise Http404("Restaurant does not exist")
	context["establishment"] = restaurant
	getRestaurantClosuresContext(context, establishment_id)
	getEstablishmentContext(context, request, establishment_id)
	return render(request, 'establishments/restaurant_detail.html', context)

def getRestaurantClosuresContext(context, establishment_id):
	closures = RestaurantClosures.db.get_by_establishment(establishment_id)
	if len(closures) != 0 :
		context["closures"] = closures

def bar_detail(request, establishment_id):
	context = user_context(request)
	user = context["user"]
	bar = Bar.db.get_by_id(establishment_id)
	if bar == None :
		raise Http404("Bar does not exist")
	context["establishment"] = bar
	getEstablishmentContext(context, request, establishment_id)
	return render(request, 'establishments/bar_detail.html', context)

def hotel_detail(request, establishment_id):
	context = user_context(request)
	user = context["user"]
	hotel = Hotel.db.get_by_id(establishment_id)
	if hotel == None :
		raise Http404("Hotel does not exist")
	context["establishment"] = hotel
	getEstablishmentContext(context, request, establishment_id)
	return render(request, 'establishments/hotel_detail.html', context)

def addSearchForm(request, context):
	if 'name' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			name_field = form.cleaned_data['name']
			name_field = '%'+name_field+'%'
			establishments = form.cleaned_data['establishments']
			tags = form.cleaned_data['tags']
			return search_results(request,name_field, establishments, tags)
	else:
		all_tags = Tag.db.get_all()
		form = SearchForm(all_tags)
	context['form'] = form

def addCommentForm(request, context={}, establishment_id=-1):
	if request.method == 'POST':
		user = get_user(request)
		if user != None:
			form = EstablishmentCommentForm(request.POST)
			establishment_id = form.data['establishment_id']
			if form.is_valid():
				score = form.cleaned_data['score']
				comment_text = form.cleaned_data['comment_text']
				written_date = datetime.datetime.now()
				try:
					EstablishmentComment.db.insert(written_date, score, comment_text, user.name, establishment_id)
				except IntegrityError: #Tried to post a comment on the same day on the same establishment
					pass
				return redirect(request, establishment_id)
			else:
				return redirect(request, establishment_id)
		else:
			return HttpResponseRedirect('/authenticate/login')
	else:
		form = EstablishmentCommentForm(initial={'establishment_id': establishment_id})
	context['add_comment_form'] = form


def addEstablishmentTagForm(request, context ={}, establishment_id=-1):
	if request.method == 'POST':
		user = get_user(request)
		if user != None:
			all_tags = Tag.db.get_all()
			form = EstablishmentTagsForm(all_tags,request.POST)
			establishment_id = form.data['establishment_id']
			if form.is_valid():
				tag_name = form.cleaned_data['tag_name']
				try:
					EstablishmentTag.db.insert(establishment_id, tag_name, user.name)
				except IntegrityError: #tried to apply the same label twice on the same establishment
					pass
				return redirect(request, establishment_id)
			else:
				return redirect(request, establishment_id)
		else:
			HttpResponseRedirect('/authenticate/login')
	else:
		all_tags = Tag.db.get_all()
		form = EstablishmentTagsForm(tags=all_tags,initial={'establishment_id': establishment_id})
	context['add_tags_form'] = form


def redirect(request, establishment_id):
	if Restaurant.db.get_by_id(establishment_id) != None:
		return HttpResponseRedirect('/establishments/restaurant/'+str(establishment_id))
	if Bar.db.get_by_id(establishment_id) != None:
		return HttpResponseRedirect('/establishments/bar/'+str(establishment_id))
	if Hotel.db.get_by_id(establishment_id) != None:
		return HttpResponseRedirect('/establishments/hotel/'+str(establishment_id))
	return HttpResponseRedirect('/establishments/')

def add_new_tag(request, establishment_id=-1):
	context = user_context(request)
	user = context["user"]
	if request.method == 'POST':
		if user != None:
			form = TagForm(request.POST)
			establishment_id = form.data['establishment_id']
			if form.is_valid():
				name = form.cleaned_data['name']
				try:
					Tag.db.insert(name)
					EstablishmentTag.db.insert(establishment_id, name, user.name)
				except:
					pass
				return redirect(request, establishment_id)
			else:
				redirect(request, establishment_id)
		else:
			HttpResponseRedirect('/authenticate/login')
	else:
		form = TagForm(initial={'establishment_id': establishment_id})
	context['add_new_tag_form'] = form
	return render(request, 'establishments/add_new_tag.html', context)

def search_results(request, name_field, establishments, tags): #For tags, return establishments who got at least one of the selected tags
	search_restaurants_list, search_bars_list, search_hotels_list = {}, {}, {}
	sqlQueryRestaurant = 'SELECT DISTINCT ON ("Restaurant".establishment_id) * FROM "Restaurant" JOIN "Establishment" ON "Restaurant".establishment_id = "Establishment".id JOIN "EstablishmentTags" on "Restaurant".establishment_id = "EstablishmentTags".establishment_id WHERE "Establishment".name LIKE %s;'
	sqlQueryBar = 'SELECT DISTINCT ON ("Bar".establishment_id) * FROM "Bar" JOIN "Establishment" ON "Bar".establishment_id = "Establishment".id JOIN "EstablishmentTags" on "Bar".establishment_id = "EstablishmentTags".establishment_id WHERE "Establishment".name LIKE %s;'
	sqlQueryHotel = 'SELECT DISTINCT ON ("Hotel".establishment_id) * FROM "Hotel" JOIN "Establishment" ON "Hotel".establishment_id = "Establishment".id JOIN "EstablishmentTags" on "Hotel".establishment_id = "EstablishmentTags".establishment_id WHERE "Establishment".name LIKE %s;'
	if len(tags) != 0:
		sqlQueryRestaurant = modifySqlQueryForTags(sqlQueryRestaurant, tags)
		sqlQueryBar = modifySqlQueryForTags(sqlQueryBar, tags)
		sqlQueryHotel = modifySqlQueryForTags(sqlQueryHotel, tags)
	with connection.cursor() as c:
		manager = BaseDBManager()
		if 'restaurants' in establishments:
			c.execute(sqlQueryRestaurant, [name_field])
			search_restaurants_list = [Restaurant.from_db(d) for d in manager.fetch_dicts(c)]
		if 'bars' in establishments:
			c.execute(sqlQueryBar, [name_field])
			search_bars_list = [Bar.from_db(d) for d in manager.fetch_dicts(c)]
		if 'hotels' in establishments:
			c.execute(sqlQueryHotel, [name_field])
			search_hotels_list = [Hotel.from_db(d) for d in manager.fetch_dicts(c)]
	context = user_context(request)
	user = context["user"]
	context["all_restaurants_list"] = search_restaurants_list
	context["all_bars_list"] = search_bars_list
	context["all_hotels_list"] = search_hotels_list
	context["title"] = 'Search results:'
	return render(request, 'establishments/index.html', context)


def results(request):
	if 'name' or 'establishments' or 'tags' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			name_field = form.cleaned_data['name']
			name_field = '%'+name_field+'%'
			establishments = form.cleaned_data['establishments']
			tags = form.cleaned_data['tags']
			return search_results(request,name_field, establishments, tags)
	else:
		form = SearchForm()
	context = user_context(request)
	user = context["user"]
	context['form'] = form
	return render(request, 'establishments/index.html', context)

def getSqlQueryFromList(givenList, sqlQuery):
	i=0
	for element in givenList:
		if i != 0:
			sqlQuery += ', '
		sqlQuery += "'"+element+"'"
		i+=1
	sqlQuery+=')'
	return sqlQuery
	
def modifySqlQueryForTags(sqlQuery, tags):
	sqlQuery = sqlQuery[:len(sqlQuery)-1]
	sqlQuery += ' AND "EstablishmentTags".tag_name IN ('
	sqlQuery = getSqlQueryFromList(tags, sqlQuery)
	sqlQuery += ';'
	return sqlQuery