from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.db import connection

from establishments.models import *
from tags.models import *
from comments.models import EstablishmentComment
from login.models import User
from common.models import BaseDBManager

from tags.forms import *
from establishments.forms import *
from comments.forms import EstablishmentCommentForm

def index(request):
	all_restaurants_list = Restaurant.db.get_all()
	all_bars_list = Bar.db.get_all()
	all_hotels_list = Hotel.db.get_all()
	context = {'all_restaurants_list': all_restaurants_list, 'all_bars_list': all_bars_list, 'all_hotels_list': all_hotels_list}
	addSearchForm(request, context)
	return render(request, 'establishments/index.html', context)

def getEstablishmentContext(context, request, establishment_id):
	#context = {'name': specific_establishment.name, 'phone_number': specific_establishment.phone_number, 'address_street': specific_establishment.address_street, 'address_number': specific_establishment.address_number, 'address_postcode': specific_establishment.address_postcode, 'address_locality': specific_establishment.address_locality, 'gps_longitude': specific_establishment.gps_longitude, 'gps_latitude': specific_establishment.gps_latitude, 'creator_name': specific_establishment.creator_name, 'created_time': specific_establishment.created_time}
	#if specific_establishment.website != "None":
	#	context['website'] = specific_establishment.website
	getTagsContext(context, establishment_id)
	getCommentsContext(context, establishment_id)
	getAverageScoreEstablishmentContext(context, establishment_id)
	addCommentForm(request, context)
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
	restaurant = Restaurant.db.get_by_id(establishment_id)
	if restaurant == None : 
		raise Http404("Restaurant does not exist")
	context = {"establishment" : restaurant}
	getRestaurantClosuresContext(context, establishment_id)
	getEstablishmentContext(context, request, establishment_id)
	return render(request, 'establishments/restaurant_detail.html', context)

def getRestaurantClosuresContext(context, establishment_id):
	closures = RestaurantClosures.db.get_by_establishment(establishment_id)
	if len(closures) != 0 :
		context["closures"] = closures

def bar_detail(request, establishment_id):
	bar = Bar.db.get_by_id(establishment_id)
	if bar == None :
		raise Http404("Bar does not exist")
	context = {"establishment" : bar}
	getEstablishmentContext(context, request, establishment_id)
	return render(request, 'establishments/bar_detail.html', context)

def hotel_detail(request, establishment_id):
	hotel = Hotel.db.get_by_id(establishment_id)
	if hotel == None :
		raise Http404("Hotel does not exist")
	context = {"establishment" : hotel}
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
		form = SearchForm()
	context['form'] = form

def addCommentForm(request, context):
	if request.method == 'POST':
		form = EstablishmentCommentForm(request.POST)
		if form.is_valid():
			return HttpResponse("Fine")
	else:
		form = EstablishmentCommentForm()
	context['add_comment_form'] = form

def search_results(request, name_field, establishments, tags): #For tags, return establishments who got at least one of the selected tags
	search_restaurants_list, search_bars_list, search_hotels_list = {}, {}, {}
	sqlQueryRestaurant = 'SELECT DISTINCT * FROM "Restaurant" JOIN "Establishment" ON "Restaurant".establishment_id = "Establishment".id JOIN "EstablishmentTags" on "Restaurant".establishment_id = "EstablishmentTags".establishment_id WHERE "Establishment".name LIKE %s;'
	sqlQueryBar = 'SELECT DISTINCT * FROM "Bar" JOIN "Establishment" ON "Bar".establishment_id = "Establishment".id JOIN "EstablishmentTags" on "Bar".establishment_id = "EstablishmentTags".establishment_id WHERE "Establishment".name LIKE %s;'
	sqlQueryHotel = 'SELECT DISTINCT * FROM "Hotel" JOIN "Establishment" ON "Hotel".establishment_id = "Establishment".id JOIN "EstablishmentTags" on "Hotel".establishment_id = "EstablishmentTags".establishment_id WHERE "Establishment".name LIKE %s;'
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
	context = {'all_restaurants_list': search_restaurants_list, 'all_bars_list': search_bars_list, 'all_hotels_list': search_hotels_list, 'title': 'Search results:'}
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

def addTest(request):
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HotelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # We will call the INSERT sql method here to add infos to the DB
            return HttpResponse("Fine")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = HotelForm()

    return render(request, 'establishments/addTest.html', {'form': form})