from django import forms

class EstablishmentCommentForm(forms.Form):
	score = forms.IntegerField(label="Score")
	comment_text = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}),label="Commentaire")