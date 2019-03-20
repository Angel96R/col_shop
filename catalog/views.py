from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Game, Author, Genre

def index(request):

    games = Game.objects.all()

    return render(
        request,
        'index.html',
        context={'games':games,},
    )

class GameListView(generic.ListView):
    model = Game    

class GameDetailView(generic.DetailView):
    model = Game
    
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')