from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from .models import *
from comments.models import Establishmentcomment
from tags.models import *
from django.db import connection
from users.models import User
from .forms import *

def index(request, context={}):
	all_restaurants_list = Restaurant.objects.raw('SELECT * FROM "Restaurant";')
	all_bars_list = Bar.objects.raw('SELECT * FROM "Bar";')
	all_hotels_list = Hotel.objects.raw('SELECT * FROM "Hotel";')
	context = {'all_restaurants_list': all_restaurants_list, 'all_bars_list': all_bars_list, 'all_hotels_list': all_hotels_list}
	#search(request, context)      I don't know why but it doesn't let meput it in another method
	if 'name' in request.GET:
		form = searchForm(request.GET)
		if form.is_valid():
			name_field = form.cleaned_data['name']
			name_field = '%'+name_field+'%'
			establishments = form.cleaned_data['establishments']
			return search_results(request,name_field, establishments)
	else:
		form = searchForm()
	context['form'] = form
	return render(request, 'establishments/index.html', context)


def restaurant_detail(request, establishment_id):
	try:
		restaurant = Restaurant.objects.raw('SELECT * FROM "Restaurant" WHERE establishment_id = %s;' , [establishment_id])[0]
		context = getEstablishmentContext(restaurant, establishment_id)
		context["price_range"] = restaurant.price_range
		context["banquet_capacity"] = restaurant.banquet_capacity
		context["take_away"] = "Yes" if restaurant.take_away else "No"
		context["delivery"] = "Yes" if restaurant.delivery else "No"
	except IndexError:  #if no restaurant is returned due to manualy input url
		raise Http404("Establishment does not exist")
	return render(request, 'establishments/restaurant_detail.html', context)

def bar_detail(request, establishment_id):
	try:
		bar = Bar.objects.raw('SELECT * FROM "Bar" WHERE establishment_id = %s;' , [establishment_id])[0]
		context = getEstablishmentContext(bar, establishment_id)
		context['smoking'] = "Yes" if bar.smoking  else "No"
		context['snack'] = "Yes" if bar.snack else "No"
	except IndexError:  #if no bar is returned due to manaly input url
		raise Http404("Establishment does not exist")
	return render(request, 'establishments/bar_detail.html', context)

def hotel_detail(request, establishment_id):
	try:
		hotel = hotel.objects.raw('SELECT * FROM "Hotel" WHERE establishment_id = %s;' , [establishment_id])[0]
		context = getEstablishmentContext(hotel, establishment_id)
		context['stars'] = hotel.stars
		context['rooms_number'] = hotel.rooms_number
		context['price_range'] = hotel.price_range
	except IndexError:  #if no hotel is returned due to manaly input url
		raise Http404("Establishment does not exist")
	return render(request, 'establishments/hotel_detail.html', context)


def getEstablishmentContext(specific_establishment, establishment_id):
	context = {'name': specific_establishment.establishment.name, 'phone_number': specific_establishment.establishment.phone_number, 'address_street': specific_establishment.establishment.address_street, 'address_number': specific_establishment.establishment.address_number, 'address_postcode': specific_establishment.establishment.address_postcode, 'address_locality': specific_establishment.establishment.address_locality, 'gps_longitude': specific_establishment.establishment.gps_longitude, 'gps_latitude': specific_establishment.establishment.gps_latitude, 'creator_name': specific_establishment.establishment.creator_name.name, 'created_time': specific_establishment.establishment.created_time}
	if specific_establishment.establishment.website != "None":
		context['website'] = specific_establishment.establishment.website
	getTagsContext(context, establishment_id)
	getCommentsContext(context, establishment_id)
	getAverageScoreEstablishmentContext(context, establishment_id)
	return context

def getCommentsContext(context, establishment_id): #Need to use this manual connection to db to handle the primary key problem
	comments_list = []
	with connection.cursor() as cursor:
		cursor.execute('SELECT written_date,score,comment_text,user_name,establishment_id FROM "EstablishmentComment" WHERE establishment_id = %s;', [establishment_id])
		for row in cursor.fetchall():
			estCom = Establishmentcomment(written_date=row[0], score=row[1], comment_text=row[2], user_name=User.objects.get(name=row[3]), establishment_id=Establishment.objects.get(id=row[4]))
			comments_list.append(estCom)
	if len(comments_list) != 0:
		context['comments_list'] = comments_list

def getAverageScoreEstablishmentContext(context, establishment_id):
	averageScore = -1
	with connection.cursor() as cursor:
		cursor.execute('SELECT avg(score) FROM "EstablishmentComment" WHERE establishment_id = %s', [establishment_id])
		row = cursor.fetchone()
		averageScore = row[0]
	if averageScore != -1:
		context['average_score'] = "{0:.2f}".format(averageScore)

def getTagsContext(context, establishment_id): #same as getCommentsContext
	tags_list = []
	tag_names_in_list = []
	tags_score = {}
	with connection.cursor() as cursor:
		cursor.execute('SELECT establishment_id, tag_name, user_name FROM "EstablishmentTags" WHERE establishment_id = %s;', [establishment_id])
		for row in cursor.fetchall():
			if row[1] not in tag_names_in_list:
				estTag = Establishmenttags(establishment_id=Establishment.objects.get(id=row[0]), tag_name=Tag.objects.get(name=row[1]), user_name=User.objects.get(name=row[2]))
				tags_list.append(estTag)
				tag_names_in_list.append(row[1])
				tags_score[row[1]] = 1
			else:
				tags_score[row[1]] += 1
	if len(tags_list) != 0 and len(tags_score) != 0:
		context['tags_list'] = tags_list
		context['tags_score'] = tags_score


def search_results(request, name_field, establishments):
	search_restaurants_list, search_bars_list, search_hotels_list = {}, {}, {}
	if 'restaurants' in establishments:
		search_restaurants_list = Restaurant.objects.raw('SELECT * FROM "Restaurant" JOIN "Establishment" ON "Restaurant".establishment_id = "Establishment".id WHERE "Establishment".name LIKE %s;', [name_field])
	if 'bars' in establishments:
		search_bars_list = Bar.objects.raw('SELECT * FROM "Bar" JOIN "Establishment" ON "Bar".establishment_id = "Establishment".id WHERE "Establishment".name LIKE %s;', [name_field])
	if 'hotels' in establishments:
		search_hotels_list = Hotel.objects.raw('SELECT * FROM "Hotel" JOIN "Establishment" ON "Hotel".establishment_id = "Establishment".id WHERE "Establishment".name LIKE %s;', [name_field])
	context = {'all_restaurants_list': search_restaurants_list, 'all_bars_list': search_bars_list, 'all_hotels_list': search_hotels_list}
	return render(request, 'establishments/index.html', context)


def results(request):
	if 'name' or 'establishments' in request.GET:
		form = searchForm(request.GET)
		if form.is_valid():
			name_field = form.cleaned_data['name']
			name_field = '%'+name_field+'%'
			establishments = form.cleaned_data['establishments']
			return search_results(request,name_field, establishments)
	else:
		form = searchForm()
	context['form'] = form
	return render(request, 'establishments/index.html', context)

def tagsFilter(search_restaurants_list, search_bars_list, search_hotels_list, tags):
	#TODO
	return