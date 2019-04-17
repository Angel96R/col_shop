from django import forms
from django.core.exceptions import ValidationError
from .models import Genre

# yes, it i taked :)
def repSymb(s, ch_old, ch_new):
    s_new  = s
    i = s_new.find(ch_old)
    while i !=-1:
        s_new = s_new[0:i] + ch_new+s_new[i+1:]
        i = s_new.find(ch_old)
    return s_new

class BuyGame(forms.Form):
    pass
    
class SearchGame(forms.Form):
    srequest = forms.CharField(label = "")
    
class FilterGenres(forms.Form):

    genres = Genre.objects.all()
    
    array = [('-1', 'Нет')]        
    
    for i in range(1, len(genres) + 1):
        array.append((genres[i - 1].id, genres[i - 1].name))

    genre = forms.ChoiceField(label = '', required = False, choices = array)