from django import forms

class searchForm(forms.Form):
	name = forms.CharField(required = False, label='Name', max_length=100)