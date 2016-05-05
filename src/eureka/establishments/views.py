from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import *
from comments.models import Establishmentcomment
from tags.models import *

def index(request):
	all_restaurants_list = Restaurant.objects.raw('SELECT * FROM "Restaurant";')
	all_bars_list = Bar.objects.raw('SELECT * FROM "Bar";')
	all_hotels_list = Hotel.objects.raw('SELECT * FROM "Hotel";')
	context = {'all_restaurants_list': all_restaurants_list, 'all_bars_list': all_bars_list, 'all_hotels_list': all_hotels_list}
	return render(request, 'establishments/index.html', context)


def restaurant_detail(request, establishment_id):
	try:
		restaurant = Restaurant.objects.raw('SELECT * FROM "Restaurant" WHERE establishment_id = %s;' , [establishment_id])[0]
		context = getEstablishmentContext(restaurant)
		#context = getCommentsContext(context, establishment_id)
		context["price_range"] = restaurant.price_range
		context["banquet_capacity"] = restaurant.banquet_capacity
		context["take_away"] = "Yes" if restaurant.take_away else "No"
		context["delivery"] = "Yes" if restaurant.delivery else "No"
	except IndexError:  #if no restaurant is returned due to manaly input url
		raise Http404("Establishment does not exist")
	return render(request, 'establishments/restaurant_detail.html', context)

def bar_detail(request, establishment_id):
	try:
		bar = Bar.objects.raw('SELECT * FROM "Bar" WHERE establishment_id = %s;' , [establishment_id])[0]
		context = getEstablishmentContext(bar)
		#context = getCommentsContext(context, establishment_id)
		context['smoking'] = "Yes" if bar.smoking  else "No"
		context['snack'] = "Yes" if bar.snack else "No"
	except IndexError:  #if no bar is returned due to manaly input url
		raise Http404("Establishment does not exist")
	return render(request, 'establishments/bar_detail.html', context)

def hotel_detail(request, establishment_id):
	try:
		hotel = hotel.objects.raw('SELECT * FROM "Hotel" WHERE establishment_id = %s;' , [establishment_id])[0]
	except IndexError:  #if no bar is returned due to manaly input url
		raise Http404("Establishment does not exist")
	return HttpResponse("You're looking at Establishment %s." % hotel.establishment.name)


def getEstablishmentContext(specific_establishment):
	context = {'name': specific_establishment.establishment.name, 'phone_number': specific_establishment.establishment.phone_number, 'address_street': specific_establishment.establishment.address_street, 'address_number': specific_establishment.establishment.address_number, 'address_postcode': specific_establishment.establishment.address_postcode, 'address_locality': specific_establishment.establishment.address_locality, 'gps_longitude': specific_establishment.establishment.gps_longitude, 'gps_latitude': specific_establishment.establishment.gps_latitude, 'creator_name': specific_establishment.establishment.creator_name.name, 'created_time': specific_establishment.establishment.created_time}
	if specific_establishment.establishment.website != "None":
		context['website'] = specific_establishment.establishment.website
	return context

def getCommentsContext(context, establishment_id): #Need to see how to handle this cause of primary key problem
	comments_list = Establishmentcomment.objects.raw('SELECT * FROM "EstablishmentComment" WHERE establishment_id = %s;', [establishment_id])
	context['comments_list'] = comments_list
	return context

def getTagsContext(context, establishment_id): #same as comments
	tags_list = Establishmenttags.objects.raw('SELECT * FROM "EstablishmentTags" WHERE establishment_id = %s;', [establishment_id])
	context['tags_list'] = tags_list
	return context