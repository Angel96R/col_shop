from django import forms
from django.core.exceptions import ValidationError

class BuyGame(forms.Form):
    pass
    
class SearchGame(forms.Form):
    srequest = forms.CharField()
    