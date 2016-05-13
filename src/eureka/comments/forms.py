from django.core.validators import *
from django import forms

class EstablishmentCommentForm(forms.Form):
	score = forms.IntegerField(label="Score", validators=[MinValueValidator(0, "Min 0"), MaxValueValidator(5, "Max 5")])
	comment_text = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}),label="Commentaire")
	establishment_id = forms.IntegerField(widget= forms.HiddenInput())
	
	# written_date = models.DateTimeField()
	# score = models.SmallIntegerField()
	# comment_text = models.TextField()
	# user_name = models.ForeignKey('login.EurekaUser', db_column='user_name')
	# establishment_id = models.ForeignKey('establishments.Establishment')