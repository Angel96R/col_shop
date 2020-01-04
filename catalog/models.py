from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin

import datetime

#### SHOPS&POINTS ####
    
class City(models.Model):

    name = models.CharField(max_length = 300)  

    def __str__(self):
        return '%s' % (self.name)
        
class Shops(models.Model):

    name = models.CharField(max_length = 200)
    
    city = models.OneToOneField(City,
        help_text = "Select a your city", 
        on_delete = models.DO_NOTHING,
        )
    
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name    
    
    #def get_absolute_url(self):
        #return reverse('game-detail', args=[str(self.id)])

        
            
#### GAMES ####

class Genre(models.Model):

    name = models.CharField('Название жанра', max_length = 200, 
        help_text = "Это может быть карточная игра, варгейм и т.п.")
    
    def __str__(self):
        return self.name
        
class Author(models.Model):

    name = models.CharField('Название разработчика', max_length = 300)
    
    def get_absolute_url(self):
        return reverse('author-detail', args = [str(self.id)])    

    def __str__(self):
        return '%s' % (self.name)

class Game(models.Model):

    title = models.CharField(max_length = 200)
    
    cost = models.DecimalField(max_digits = 10, decimal_places = 2, 
        default = 0, blank = True, null = True)
    
    image = models.ImageField(upload_to = 'images/',
        null = True, blank = True)
    
    author = models.ForeignKey('Author',
        on_delete = models.SET_NULL, null = True, blank = True)
    
    summary = models.TextField(null = True, blank = True)        
    
    genre = models.ManyToManyField(Genre,
        help_text = "Зажмите Ctrl для выбора нескольких",
        blank = True, null = True)
        
    date_create = models.DateField(auto_now_add = True, null = True, blank = True)
    date_update = models.DateField(auto_now = True, null = True, blank = True)
    by_create = models.DecimalField(max_digits = 10, decimal_places = 0, default = 0, 
        blank = True, null = True)
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('game-detail', args = [str(self.id)])
        
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        
    display_genre.short_description = 'Genre' 
    
    
class Check(models.Model):

    name = models.CharField(max_length = 200, blank = True, null = True,
        help_text = "ФИО покупателя, необязательно", default = '-')
    user_id = models.DecimalField(max_digits = 10, decimal_places = 0, default = 0,
        blank = True, null = True)
    games = models.ManyToManyField(Game,
        help_text = "Зажмите Ctrl для выбора нескольких")
    mail = models.CharField(max_length = 200, blank = True, null = True,
        default = '-')
    mobile = models.CharField(max_length = 12, blank = True, null = True,
        default = '-')
    cost = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0,
        help_text = "Стоимость заказа посчитается автоматически, но вы можете вести сами")
    status = models.CharField(max_length = 200, default = "Не оплачен", blank = True, null = True)
    date_create = models.DateTimeField(auto_now_add = True, null = True, blank = True)
    address = models.CharField(max_length = 333, default = '-', blank = True,
        help_text = "Адрес покупателя, необязательно")    
    counts = models.CharField(max_length = 200, blank = True, null = True, default = '-')
    completed = models.BooleanField(default = False)
    completed_date = models.DateTimeField(null = True, blank = True)
    
class Gathering(models.Model):

    address = models.CharField(max_length = 333, default = '-', blank = True,
        help_text = "Адрес мероприятия")        
    date = models.DateTimeField(null = True, blank = True)
    name = models.CharField(max_length = 200, blank = True, null = True,
        help_text = "Название мероприятия, необязательно", default = '-')
    summary = models.CharField(max_length = 1000, blank = True, null = True,
        help_text = "Описание мероприятия, необязательно", default = '-')
        
    # TUT TIPO ESHE DA POLE IS BE
        
class EditGameModelForm(ModelForm):
    
    class Meta:
    
        model = Game
        fields = '__all__'
    
#### CUSTOMER&SHOP ####



class Customer(models.Model):
    
    name = models.CharField("Логин покупателя", max_length = 300)
    user = models.OneToOneField(User, on_delete = models.DO_NOTHING)
    
    # store employee
    super_customer = models.BooleanField("Сотрудник", default = False)        
    super_was = models.BooleanField("Был сотрудником", default = False)         
    super_staffedit = models.BooleanField("Редактирование сотрудников", default = False)
    super_edititems = models.BooleanField("Редактирование товаров", default = False)
    super_aboutedit = models.BooleanField("Редактирование 'мы'", default = False)
          

    def __str__(self):
        return '%s' % (self.name)

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()        
        
class Cart(models.Model):

    items = models.ManyToManyField(Game)
    customer = models.ForeignKey(Customer, on_delete = models.DO_NOTHING)

    def __str__(self):
        return '%s' % (self.id)
    
#### IMAGES ####

class Gallery(models.Model):
    
    image = models.ImageField(upload_to = 'images/',
        null = True, blank = True)
    game = models.ForeignKey(Game, on_delete = models.DO_NOTHING)
	
class InfoSite(models.Model):
	
    desc = models.CharField(max_length = 1000, blank = True, null = True)
    link_vk = models.CharField(max_length = 255, blank = True, null = True)
    link_fb = models.CharField(max_length = 255, blank = True, null = True)
    link_tw = models.CharField(max_length = 255, blank = True, null = True)
  
class Meet(models.Model):
    
    date = models.DateTimeField(null = True, blank = True)
    name = models.CharField(max_length = 300) 
    address = models.CharField(max_length = 300, default = "-")
    summary = models.CharField(max_length = 1000)
    users = models.ManyToManyField(User, 
        related_name='users',
        help_text = "Зажмите Ctrl для выбора нескольких",
        blank = True, null = True)
    games = models.ForeignKey(Game, on_delete = models.SET_NULL,
        blank = True, null = True)     
    lead = models.ForeignKey(User,
        on_delete = models.SET_NULL, null = True, blank = True)