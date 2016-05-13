from django import forms
from .models import Tag

class TagForm(forms.Form):
	name = forms.CharField(required=True, max_length=16, label="Name")
	establishment_id = forms.IntegerField(widget= forms.HiddenInput()) #used to redirect to the good page

class EstablishmentTagsForm(forms.Form):
	all_tags = Tag.db.get_all()
	
	TAG_OPTIONS = ()
	for tag in all_tags:
	 	TAG_OPTIONS = TAG_OPTIONS + ((tag.name, tag.name),)
	tag_name = forms.ChoiceField(label="Choose the label to apply", choices=TAG_OPTIONS)
	establishment_id = forms.IntegerField(widget= forms.HiddenInput())