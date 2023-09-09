from django import forms

class ParkSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Parks', max_length=100)
