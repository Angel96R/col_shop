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
from .forms import FilterGenres

def index(request):

    games = Game.objects.all()   
    genres = Genre.objects.all()    

    return render(
        request,
        'index.html',
        context = {'games' : games, 'genres' : genres},
    )
    
def getGames(request):

    search_form = SearchGame()
    genres_form =  FilterGenres()
    genres = Genre.objects.all()
    games = Game.objects.all()
    genres = Genre.objects.all()
    
    genre = request.GET.get('genre')
    srequest = request.GET.get('srequest')

    if genre != None:
        if genre != "-1":        
            games = Game.objects.filter(genre = int(genre))
            
    if srequest != None:
        games = Game.objects.filter(title = srequest)
           
    return render(
        request,
        'catalog/game_list.html',
        context = {'game_list' : games, 
        'form' : search_form,
        'genres' : genres,
        'genres_form' : genres_form,
        },
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


    if request.user.is_authenticated:

        try:
            user_cart = Cart.objects.get(customer = request.user.customer)
            cart_items = user_cart.items.all()
        except Cart.DoesNotExist:
            user_cart = None
            cart_items = None
            
    else:
    
        try:
            user_cart = request.session.get('cart', {})
            cart_items = []
            for i in user_cart:
                cart_items.append(Game.objects.get(pk = user_cart[i]))
        except Cart.DoesNotExist:
            pass
        
    return render(request, 'catalog/cart.html', 
        {'user_cart' : user_cart, 'cart_items' : cart_items}
    )
    
def dellFromCart(request, pk):

    if request.user.is_authenticated:

        user_cart = Cart.objects.get(customer = request.user.customer)
        item = user_cart.items.get(id = pk)
        user_cart.items.remove(item)
        
    else:
    
        user_cart = request.session.get('cart', {})        
        user_cart.pop(pk)        
    
    return getCart(request)
    
def addToCart(request, pk):

    repath = request.GET.get('repath')
    
    game = Game.objects.get(pk = pk)
    
    if request.user.is_authenticated:
        user_cart = Cart.objects.get(customer = request.user.customer)
        user_cart.items.add(game)
    else:
        user_cart = request.session.get('cart', {})
        user_cart[pk] = pk
        request.session['cart'] = user_cart
    
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

