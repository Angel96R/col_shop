from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



#### SHOPS&POINTS ####



class City(models.Model):

    name = models.CharField(max_length = 300)  

    def __str__(self):
        return '%s' % (self.name)
        
class Shops(models.Model):

    name = models.CharField(max_length = 200)
    
    city = models.ManyToManyField(City,
        help_text = "Select a your city")
    
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title    
    
    #def get_absolute_url(self):
        #return reverse('game-detail', args=[str(self.id)])

        
            
#### GAMES ####



class Genre(models.Model):

    name = models.CharField(max_length = 200, 
        help_text = "Enter a game genre (e.g. Wargame, Card etc.)")
    
    def __str__(self):
        return self.name
        
class Author(models.Model):

    name = models.CharField(max_length = 300)
    
    def get_absolute_url(self):
        return reverse('author-detail', args = [str(self.id)])    

    def __str__(self):
        return '%s' % (self.name)

class Game(models.Model):

    title = models.CharField(max_length = 200)
    
    image = models.ImageField(upload_to = 'images/',
        null = True, blank = True)
    
    author = models.ForeignKey('Author',
        on_delete = models.SET_NULL, null = True)
    
    summary = models.TextField(max_length = 1000,
        help_text = "Enter a brief description of the game")
    
    genre = models.ManyToManyField(Genre,
        help_text = "Select a genre for this game")
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('game-detail', args = [str(self.id)])
        
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        
    display_genre.short_description = 'Genre' 
    
    
    
#### CUSTOMER&SHOP ####



class Customer(models.Model):
    
    name = models.CharField(max_length = 300)
    user = models.OneToOneField(User, on_delete = models.DO_NOTHING) 

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
    