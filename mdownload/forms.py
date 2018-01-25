from django import forms

#simple manga search form in the index page
class SearchForm(forms.Form):
	search_input = forms.CharField(max_length=200,label='')
