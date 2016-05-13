from django import forms
from tags.models import Tag
from establishments.models import *

class SearchForm(forms.Form):
	EST_OPTIONS = (
            ("restaurants", "Restaurants"),
            ("bars", "Bars"),
            ("hotels", "Hotels"),
            )

	all_tags = Tag.db.get_all()
	
	TAG_OPTIONS = ()
	for tag in all_tags:
		TAG_OPTIONS = TAG_OPTIONS + ((tag.name, tag.name),)
	establishments = forms.MultipleChoiceField(required = False, label= 'Establishments', widget=forms.CheckboxSelectMultiple, choices=EST_OPTIONS, initial=[c[0] for c in EST_OPTIONS])
	tags = forms.MultipleChoiceField(required = False, label= 'Tags', widget=forms.CheckboxSelectMultiple, choices=TAG_OPTIONS)
	name = forms.CharField(required = False, label='Name', max_length=100)

class EstablishmentForm(forms.Form):
	name = forms.CharField(max_length=64, label="Name")
	address_street = forms.CharField(max_length=64, label= "Street")
	address_number = forms.IntegerField(label="Number")
	address_postcode = forms.IntegerField(label="Postcode")
	address_locality = forms.CharField(max_length=32, label="Locality")
	gps_longitude = forms.DecimalField(max_digits=12, decimal_places=8, label="Longitude")
	gps_latitude = forms.DecimalField(max_digits=12, decimal_places=8, label="Latitude")
	phone_number = forms.CharField(max_length=16, label="Phone number")
	website = forms.URLField(max_length=255, required=False, label="Website")

	#creator_name = models.ForeignKey('login.EurekaUser', db_column='creator_name')
	#created_time = models.DateField()

class HotelForm(EstablishmentForm):
	stars = forms.IntegerField(required=True, label= "Stars")
	rooms_number = forms.IntegerField(required = True, label = "Rooms number")
	price_range = forms.DecimalField(required = True, label = "Price range", max_digits=6, decimal_places=2)


class BarForm(EstablishmentForm):
	smoking = forms.BooleanField(required=False,label="Smoking")
	snack = forms.BooleanField(required=False,label="Snack")

class RestaurantForm(EstablishmentForm): 
	price_range = forms.DecimalField(required = True, label = "Price range", max_digits=6, decimal_places=2)
	banquet_capacity = forms.IntegerField(required = True, label = "Banquet capacity")
	take_away = forms.BooleanField(required = False,label="Take away")
	delivery = forms.BooleanField(required=False,label="Delivery")
	#TODO HANDLE CLOSURES