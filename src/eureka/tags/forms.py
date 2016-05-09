from django import forms
from .models import Tag

class TagForm(forms.Form):
	name = forms.CharField(required=True, max_length=16, label="Name")

class EstablishmentTagsForm(forms.Form):
	all_tags = Tag.objects.raw('SELECT * FROM "Tag";')
	
	TAG_OPTIONS = ()
	for tag in all_tags:
		TAG_OPTIONS = TAG_OPTIONS + ((tag.name, tag.name),)
	name = forms.ChoiceField(label="Choose the label to apply", choices=TAG_OPTIONS)