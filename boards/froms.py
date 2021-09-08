from django import forms
from .models import Board

class AddNewBoard(forms.ModelForm):
	name=forms.CharField(
		widget=forms.TextInput(
			attrs={'placeholder': 'Enter Board name here'}
			),
		max_length=50,help_text="Board name")

	description = forms.CharField(widget=forms.Textarea(
		attrs={'rows':3,'placeholder':'Enter Board description here'}
	),max_length=300,help_text="max length 300 letter")

	class Meta:
		model=Board
		fields=['name','description']