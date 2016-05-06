from django import forms
from tags.models import Tag

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
