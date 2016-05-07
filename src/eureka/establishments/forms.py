from django import forms
from tags.models import Tag
from .models import *

class searchForm(forms.Form):
	EST_OPTIONS = (
            ("restaurants", "Restaurants"),
            ("bars", "Bars"),
            ("hotels", "Hotels"),
            )
	all_tags = Tag.objects.raw('SELECT * FROM "Tag";')
	
	TAG_OPTIONS = ()
	for tag in all_tags:
		TAG_OPTIONS = TAG_OPTIONS + ((tag.name, tag.name),)
	establishments = forms.MultipleChoiceField(required = False, label= 'Establishments', widget=forms.CheckboxSelectMultiple, choices=EST_OPTIONS, initial=[c[0] for c in EST_OPTIONS])
	tags = forms.MultipleChoiceField(required = False, label= 'Tags', widget=forms.CheckboxSelectMultiple, choices=TAG_OPTIONS)
	name = forms.CharField(required = False, label='Name', max_length=100)

class EstablishmentForm(forms.ModelForm):
	class Meta:
		model = Establishment
		fields = ['name', 'address_street', 'address_number','address_postcode','address_locality', 'gps_longitude', 'gps_latitude', 'phone_number', 'website']

class HotelForm(EstablishmentForm):
	stars = forms.IntegerField(required=True, label= "Stars")
	rooms_number = forms.IntegerField(required = True, label = "Rooms number")
	price_range = forms.DecimalField(required = True, label = "Price range", max_digits=6, decimal_places=2)

class BarForm(EstablishmentForm):
	smoking = forms.BooleanField(required=True, label="Smoking")
	snack = forms.BooleanField(required=True, label="Snack")

#class RestaurantForm(EstablishmentForm):  --- Need to see how to handle restaurant closures