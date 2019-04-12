from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.models import User
from .models import Game, Author, Genre, Customer, Cart
from .forms import BuyGame
from .forms import SearchGame

def index(request):

    games = Game.objects.all()
    

    return render(
        request,
        'index.html',
        context = {'games' : games, },
    )
    
def getGames(request):

    games = Game.objects.all()
    search_form = SearchGame()
    
    return render(
        request,
        'catalog/game_list.html',
        context = {'game_list' : games, 
        'form' : search_form, },
    )
    
def searchGame(request):

    games = Game.objects.all()        
    search_form = SearchGame(request.GET)

    return render(
        request,
        'catalog/game_search.html',
        context = {'game_list' : games, 
        'form' : search_form, },
    )

def getGame(request, pk):

    game = Game.objects.get(pk = pk)
    
    form = BuyGame()

    if request.method == 'POST':
    
        form = BuyGame(request.POST)
        
        try:
            be_cart = Cart.objects.get(customer = request.user.customer)
        except Cart.DoesNotExist:
            be_cart = None
        
        if(be_cart != None):
            be_cart.items.add(game)
        else:
            new_cart = Cart()
            new_cart.customer = request.user.customer
            new_cart.save()
            new_cart.items.add(game)
        
    return render(request, 'catalog/game_detail.html', 
        {'form': form, 'game' : game}
    )
    
def getCart(request):

    try:
        user_cart = Cart.objects.get(customer = request.user.customer)
        cart_items = user_cart.items.all()
    except Cart.DoesNotExist:
        user_cart = None
        cart_items = None
        
    return render(request, 'catalog/cart.html', 
        {'user_cart' : user_cart, 'cart_items' : cart_items}
    )
    
def dellFromCart(request, pk):

    user_cart = Cart.objects.get(customer = request.user.customer)
    item = user_cart.items.get(id = pk)
    user_cart.items.remove(item)
    
    return getCart(request)
    
def addToCart(request, pk):

    repath = request.GET.get('repath')

    game = Game.objects.get(pk = pk)

    user_cart = Cart.objects.get(customer = request.user.customer)
    user_cart.items.add(game)
    
    return HttpResponseRedirect(repath)

class GameListView(generic.ListView):
    model = Game    
    
### AUTHORS ###
    
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    
### OLD ###
    
#class GameDetailView(generic.DetailView):

    #model = Game
        
    #def get_context_data(self, **kwargs):

        #context = super(GameDetailView, self).get_context_data(**kwargs)

        #context['form'] = BuyGame()
        #return context

