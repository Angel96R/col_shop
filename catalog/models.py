from django.db import models
from django.urls import reverse

class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Enter a game genre (e.g. Wargame, Card etc.)")
    
    def __str__(self):
        return self.name
		
class City(models.Model):

    name = models.CharField(max_length=300)  

    def __str__(self):
        return '%s' % (self.name)

class Game(models.Model):

    title = models.CharField(max_length=200)
    
    image = models.ImageField(upload_to='images/',
        null=True, blank=True)
    
    author = models.ForeignKey('Author',
        on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000,
        help_text="Enter a brief description of the game")
    
    genre = models.ManyToManyField(Genre,
        help_text="Select a genre for this game")
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('game-detail', args=[str(self.id)])
        
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        
    display_genre.short_description = 'Genre'
    
class Shops(models.Model):

    name = models.CharField(max_length=200)
    
    city = models.ManyToManyField(City,
        help_text = "Select a your city")
    
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title    
    
    #def get_absolute_url(self):
        #return reverse('game-detail', args=[str(self.id)])
        
class Author(models.Model):

    name = models.CharField(max_length=300)
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])    

    def __str__(self):
        return '%s' % (self.name)