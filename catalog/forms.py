from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from .models import Genre
from .models import Game

import datetime

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
    
    srequest = forms.CharField(required = False, label = "")
    
    genres = Genre.objects.all()
    
    array = [('-1', 'Нет')]        
    
    for i in range(1, len(genres) + 1):
        array.append((genres[i - 1].id, genres[i - 1].name))

    genre = forms.ChoiceField(label = '', required = False, choices = array)
    
    
class GalleryGameForm(forms.Form):
        
    image01 = forms.FileInput()
    image02 = forms.FileInput()
        
class TimeReport(forms.Form):
    
    date_start = forms.DateTimeField(error_messages={'invalid': 'Пожалуйста, либо оставьте поля полностью пустыми, либо укажите все данные'}, required = False,
        label = "Начало периода", widget=forms.SelectDateWidget(years=range(2018, datetime.datetime.now().year + 1)))
    date_end = forms.DateTimeField(error_messages={'invalid': 'Пожалуйста, либо оставьте поля полностью пустыми, либо укажите все данные'}, required = False, label = "Конец периода", widget=forms.SelectDateWidget(years=range(2018, datetime.datetime.now().year + 1)))
    only_completed = forms.BooleanField(required = False, label = "Только завершенные")
    
class InfoSiteForm(forms.Form):
    
    desc = forms.CharField(required = False, max_length = 1000, label = "Описание")
    link_vk = forms.CharField(required = False, max_length = 255, label = "Ссылка на Вконтакте")
    link_fb = forms.CharField(required = False, max_length = 255, label = "Ссылка на Facebook")
    link_tw = forms.CharField(required = False, max_length = 255, label = "Ссылка на Twitter")
    
class MeetForm(forms.Form):

    games = Game.objects.all()
    staff = User.objects.filter(is_staff = True)
    
    array = []
    arr_lead = []    
    
    print("#############")
    for i in range(len(games)):
        print(games[i].id)
        array.append((games[i].id, games[i].title))
        
    for i in range(len(staff)):
        arr_lead.append((staff[i].id, staff[i].last_name + ' ' + staff[i].first_name))
        
    datetime = forms.DateTimeField(
        error_messages={'invalid': 'Пожалуйста, заполните'},
        label = "Время проведения",         
        help_text = "Введите в формате ГГГГ-ММ-ДД ЧЧ:ММ",
        initial=format(datetime.date.today(),'%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.TimeInput(format='%H:%M'),        
    )
            
    name = forms.CharField(max_length = 300, label = "Название мероприятия") 
    summary = forms.CharField(max_length = 1000, label = "Описание мероприятия")    
    game = forms.ChoiceField(label = 'Основная игра', choices = array)
    #forms.MultipleChoiceField(required = False, label = 'Игры', choices = array)
    address = forms.CharField(max_length = 300, label = "Адрес мероприятия")     
    lead = forms.ChoiceField(label = 'Ответственный', choices = arr_lead)
    
class ProfileForm(forms.Form):

    last_name = forms.CharField(max_length = 300, label = "Фамилия") 
    first_name = forms.CharField(max_length = 300, label = "Имя") 
    mail = forms.EmailField(label = "Почта")
    
