from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm, SelectDateWidget
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from .models import Game, Author, Genre, Customer, Cart, Gallery, Check, InfoSite, Meet

from .forms import BuyGame
from .forms import SearchGame
from .forms import GalleryGameForm
from .forms import TimeReport
from .forms import InfoSiteForm
from .forms import MeetForm
from .forms import ProfileForm

from .site_classes import PageClass
from .site_classes import SiteClass

from django.conf import settings

import datetime

site = SiteClass()

class RegisterFormView(FormView):

    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/catalog/games/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()        

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

def goRepath(request):

    repath = request.GET.get('repath')
    return HttpResponseRedirect(repath)

def index(request):

    games = Game.objects.all()   
    genres = Genre.objects.all()    

    return render(
        request,
        'index.html',
        context = {'games' : games, 'genres' : genres},
    )
    
def getCartsOfShop(request):

    if request.user.is_staff:
        
        carts = Cart.objects.filter(customer__super_shop = request.user.customer.super_shop)
        
        return render(request, 'adminp/carts_shop.html', {'carts' : carts})
            
    else:
        
        return HttpResponseForbidden()

def getCartOfShop(request, pk):

    pass
    
def getStaffOfShop(request):

    if request.user.is_staff:
        
        customers = Customer.objects.all()
        users = User.objects.all()
        f_users = []
                
        for i in range(len(users)):
            
            if(users[i].customer.super_customer == True):                
                f_users.append(users[i])
        
        return render(request, 'adminp/staff_shop.html', {'users' : f_users})
            
    else:
        
        return HttpResponseForbidden()
        
def getGamesToAdmin(request):

    if request.user.is_staff:
                
        games = Game.objects.all()    
        by_create_users = {}
        
        for i in range(len(games)):
        
            try:
                user = User.objects.get(id = int(games[i].by_create))
                games[i].user_create = user.first_name + " " + user.last_name
            except User.DoesNotExist:
                games[i].user_create = "Удален"                        
        
        return render(request, 'adminp/games.html', {
            'site' : site, 'games' : games,
            'users_create' : by_create_users
        })
            
    else:
        
        return HttpResponseForbidden()
        
def getCheckoutPanel(request):
    
    return render(request, 'adminp/checkout.html', {
            'site' : site
        })

def removeEmployee(request, pk):

    if request.user.is_staff:
    
        repath = request.GET.get('repath')
        
        if request.user.customer.super_staffedit:
        
            employee = Customer.objects.get(id = pk)
            employee.super_customer = False            
            employee.save()
            
            employee_user = User.objects.get(id = employee.id)
            employee_user.is_staff = False
            employee_user.save()
        
        return HttpResponseRedirect(repath)
        
    else:
        
        return HttpResponseForbidden()
        
def delGame(request, pk):

    if request.user.is_staff:
    
        repath = request.GET.get('repath')
       
        Gallery.objects.filter(game = pk).delete()
	   
        Game.objects.filter(pk = pk).delete()
        
        return HttpResponseRedirect(repath)
        
    else:
        
        return HttpResponseForbidden() 
    
def getGames(request):

    search_form = SearchGame(request.GET)
    genres = Genre.objects.all()
    games = Game.objects.all()
    genres = Genre.objects.all()
    
    page_sets = PageClass()
    page_sets.genre = None
    
    genre = request.GET.get('genre')
    srequest = request.GET.get('srequest')

    if genre != None:
        if genre != "-1":        
            try:
                games = games.filter(genre = int(genre))
            except ValueError:
                pass
        page_sets.genre = genre
                
    if srequest != None:
        games = games.filter(title__contains = srequest)          
    
    paginator = Paginator(games, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    games_page = paginator.get_page(page)

    return render(
        request,
        'catalog/game_list.html',
        context = {
            'game_list' : games_page, 
            'form' : search_form,
            'genres' : genres,
            'page_sets' : page_sets,
            'srequest' : srequest,
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
    images = Gallery.objects.filter(game = pk)
    
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
        {'form': form, 'game' : game, 'images' : images}
    )
    
class GalleryCreate(CreateView):

    model = Gallery
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('game_update', kwargs={'pk': self.object.game.id})
        
class CheckCreate(CreateView):

    model = Check
    fields = '__all__'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super(CheckCreate, self).dispatch(request, *args, **kwargs)
    
    def CheckCreate(self):
        model.user_id = 0        
        models.status = "Не оплачен"
    
    def clean(self):
        model.user_id = 0
        models.status = "Не оплачен"
    
    def get_success_url(self):
        return reverse('check_sum', kwargs={'pk': self.object.id})         
        
def sumCheck(request, pk):

    check = Check.objects.get(id = pk)
    check_orig = Check.objects.get(id = pk)
    check = check.games.all()

    if request.method == 'POST':
    
        counts_str = "";
        
        if(request.POST.get('pay_status') == 'payed'):
            check_orig.status = "Оплачен"
        else:
            check_orig.status = "Не оплачен"
    
        for i in range(len(check)):
            counts_str = counts_str + str(check[i].id) + "_" + request.POST.get("count_" + str(check[i].id)) + "_"
            
        check_orig.counts = counts_str
                
        game_ids = []
        game_counts = []

        is_id = True
        
        sum = 0
    
        for value in check_orig.counts.split('_'):
            if(is_id == True):
                game_ids.append(value)
                is_id = False
            else:
                game_counts.append(value)
                is_id = True
        
        for i in range(len(game_ids) - 1):
            for j in range(len(check)):
                if(check[j].id == float(game_ids[i])):
                    check[j].count = game_counts[i]
                    sum = sum + float(check[j].count) * float(check[j].cost)
        
        check_orig.cost = sum
        check_orig.save()
            
        return HttpResponseRedirect(reverse('check_view_admin', kwargs={'pk': pk}))
        
    else:            
        
        return render(request, 'adminp/check_sum.html', {'check_orig' : check_orig, 
            'check' : check})
            
def checkViewAdmin(request, pk):
    
    check = Check.objects.get(id = pk)
    games = check.games.all()
    game_ids = []
    game_counts = []
    
    is_id = True
    
    for value in check.counts.split('_'):
        if(is_id == True):
            game_ids.append(value)
            is_id = False
        else:
            game_counts.append(value)
            is_id = True
            
    for i in range(len(game_ids) - 1):
        for j in range(len(games)):
            if(games[j].id == float(game_ids[i])):
                games[j].count = game_counts[i]
                games[j].sum = float(games[j].count) * float(games[j].cost)
    
    return render(request, 'adminp/check_view.html', 
        {'check' : check, 'games' : games}
    )
    
    
def getAdmin(request):

    if request.user.is_staff:
            
        return render(request, 'adminp/index.html', {})
            
    else:
        
        return HttpResponseForbidden()     
        
class GameUpdate(UpdateView):

    model = Game
    fields = '__all__'    
    
    def get_success_url(self):
        return reverse('adminp-games', kwargs={})
        
class GameCreate(CreateView):

    model = Game
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('adminp-games', kwargs={})
		
class GameDelete(DeleteView):

    model = Game
    fields = '__all__'    
    
    def get_success_url(self):
        return reverse('game_view', kwargs={'pk': game.id})
        
def getCheckToClient(request, pk):

    check = Check.objects.get(pk = pk)
    games = check.games.all()
    
    game_ids = []
    game_counts = []
    
    is_id = True
    
    for value in check.counts.split('_'):
        if(is_id == True):
            game_ids.append(value)
            is_id = False
        else:
            game_counts.append(value)
            is_id = True
            
    for i in range(len(game_ids) - 1):
        for j in range(len(games)):
            if(games[j].id == float(game_ids[i])):
                games[j].count = game_counts[i]
                games[j].sum = float(games[j].count) * float(games[j].cost)                
     
    check.sum = 0
                
    for i in range(len(game_ids) - 1):
            for j in range(len(games)):
                if(games[j].id == float(game_ids[i])):
                    games[j].count = game_counts[i]
                    check.sum = check.sum + float(games[j].count) * float(games[j].cost)

    return render(request, 'catalog/check.html', 
            {'check' : check, 'games' : games}
        )
    

def getCart(request):    
    
    if request.method == 'POST':
    
        user_cart = None
        cart_items = []
        counts_str = ""
        
        try:
            user_cart = request.session.get('cart', {})            
            for i in user_cart:
                cart_items.append(Game.objects.get(pk = user_cart[i]))
        except Cart.DoesNotExist:
            pass
        
        new_check = Check()
        
        for i in range(len(cart_items)):
            print("@")
            print(cart_items[i].id)
        
        new_check.save()
        
        for i in range(len(cart_items)):
            new_check.games.add(cart_items[i])
            
        for i in range(len(cart_items)):
            counts_str = counts_str + str(cart_items[i].id) + "_" + request.POST.get("count_" + str(cart_items[i].id)) + "_"
            
        new_check.counts = counts_str
                
        game_ids = []
        game_counts = []

        is_id = True
        
        sum = 0
    
        for value in new_check.counts.split('_'):
            if(is_id == True):
                game_ids.append(value)
                is_id = False
            else:
                game_counts.append(value)
                is_id = True
        
        for i in range(len(game_ids) - 1):
            for j in range(len(cart_items)):
                if(cart_items[j].id == float(game_ids[i])):
                    cart_items[j].count = game_counts[i]
                    sum = sum + float(cart_items[j].count) * float(cart_items[j].cost)
        
        new_check.cost = sum
        
        new_check.name = request.POST.get("name")
        new_check.address = request.POST.get("address")
        new_check.mobile = request.POST.get("tel")
        new_check.mail = request.POST.get("mail")
        new_check.user_id = request.POST.get("user_id")        
        new_check.save()
        del request.session['cart']
        
        return HttpResponseRedirect(reverse('check_view_client', kwargs={'pk': new_check.id}))
        
    else:
    
        checks = None
    
        if request.user.is_authenticated:
            checks = Check.objects.filter(user_id = request.user.id, 
                completed = False)
    
        try:
            user_cart = request.session.get('cart', {})
            cart_items = []
            for i in user_cart:
                cart_items.append(Game.objects.get(pk = user_cart[i]))
                            
        except Cart.DoesNotExist:
            pass
            
        return render(request, 'catalog/cart.html', 
            {'checks' : checks, 
            'user_cart' : user_cart, 'cart_items' : cart_items}
        )
    
def dellFromCart(request, pk):

    #if request.user.is_authenticated:

    #    user_cart = Cart.objects.get(customer = request.user.customer)
    #    item = user_cart.items.get(id = pk)
    #    user_cart.items.remove(item)
        
    #else:
    
    user_cart = request.session.get('cart', {})        
    user_cart.pop(pk)        
    
    return getCart(request)
    
def addToCart(request, pk):

    repath = request.GET.get('repath')
    
    game = Game.objects.get(pk = pk)
    
    #if request.user.is_authenticated:
    #    user_cart = Cart.objects.get(customer = request.user.customer)
    #    user_cart.items.add(game)
    #else:
    user_cart = request.session.get('cart', {})
    user_cart[pk] = pk
    request.session['cart'] = user_cart
    
    return HttpResponseRedirect(repath)
    
def getChecksNonCompletes(request, status = 0):

    checks = Check.objects.filter(completed = False)
    
    return render(request, 'adminp/check_non_comps.html', 
            {'checks' : checks, 'status' : status}
        )

class GameListView(generic.ListView):
    model = Game    
    
def delCheck(request, pk):

    repath = request.GET.get('repath')               

    check = Check.objects.get(pk = pk)
    check.delete()    
    
    return HttpResponseRedirect(repath)
    
def compCheck(request, pk):

    check = Check.objects.get(pk = pk)
    check.completed = True
    check.completed_date = datetime.datetime.today()
    check.save()
    
    return getChecksNonCompletes(request, 2)
    
def getCheckHistory(request):

    checks = Check.objects.filter(completed = True)
   
    page_sets = PageClass()            
    
    paginator = Paginator(checks, 10)
    page = request.GET.get('page')
    checks_page = paginator.get_page(page)

    return render(
        request,
        'adminp/check_history.html',
        context = {
            'checks' : checks,
            'checks_page' : checks_page, 
        },
    )
    
def getChecksReport(request):

    form = TimeReport(request.POST)    
    
    checks = None
    
    sum = 0
    count = 0
    
    if request.method == 'POST':
        
        try:
            if(form.date_start == None):
                pass
        except AttributeError:
            form.date_start = "1999-01-01"
            
        try:
            if(form.date_end == None):
                pass
        except AttributeError:
            form.date_end = datetime.datetime.today()
            
        try:
            if(form.only_completed == None):
                pass
        except AttributeError:
            form.only_completed = False

        if(request.POST.get('only_completed') == 'on'):
            checks = Check.objects.filter(completed_date__range = [form.date_start, form.date_end], completed = True)            
        else:
            checks = Check.objects.filter(
                Q(completed_date__range = [form.date_start, form.date_end]) | Q(completed_date = None)
            )
            
        for i in range(len(checks)):
            sum = sum + checks[i].cost
            
        count = len(checks)
        
    return render(
        request,
        'adminp/check_report.html',
        context = {
            'form' : form,
            'checks' : checks,
            'sum' : sum,
            'count' : count,
        },
    )
    
def setAbout(request):

    try:
        info = InfoSite.objects.get(pk = 18)
    except InfoSite.DoesNotExist:
        info = InfoSite()
        info.save()
    
    return render(
        request,
        'about.html',
        context = {
            'info' : info,
        },
    )
    
def InfoSiteUpdate(request):

    if request.user.customer.super_aboutedit == True:

        try:
            info = InfoSite.objects.get(pk = 18)
        except InfoSite.DoesNotExist:
            info = InfoSite()
            info.save()        
            
        form = InfoSiteForm(request.POST)        

        if request.method == 'POST':
        
            info.desc = form.data['desc']
            info.link_vk = form.data['link_vk']
            info.link_fb = form.data['link_fb']
            info.link_tw = form.data['link_tw']
            
            info.save()
        
            return HttpResponseRedirect(reverse('about', kwargs={}))
            
        return render(
            request,
            'about_edit.html',
            context = {
                'form' : form,
            },
        )
        
    else:
    
        return HttpResponseForbidden()
        
def getMeets(request, status = 0):

    meets = Meet.objects.filter(
    
        date__gte = datetime.datetime.today()
    
    ) 
    
    
    for i in range(len(meets)):        
        meets[i].count = len(meets[i].users.all())  
        
        try:
            user_is = meets[i].users.get(id = request.user.id)
            meets[i].status = "Вы учавствуете"
        except User.DoesNotExist:
            meets[i].status = "Учавствовать"
        
        try:
            game = Game.objects.get(id = meets[i].games.id)        
            meets[i].image = game.image
        except AttributeError:
            pass
    
    return render(
        request,
        'meets.html',
        context = {
            'meets' : meets,
            'status' : status,
        },
    )
    
def MeetAdd(request):
    
    form = MeetForm(request.POST)
    
    if request.method == 'POST':
    
        meet = Meet()        
        meet.save()
        meet.date = form.data['datetime']
        meet.name = form.data['name']
        meet.address = form.data['address']
        meet.summary = form.data['summary']         
        meet.lead = User.objects.get(pk = int(form.data['lead']))
        
        game = Game.objects.get(id = int(form.data['game']))
        meet.games = game
        
        #print("@@@@@@@@@@@@@@")
        #if form.is_valid():
        
        #picked = form.data.get('games')    
            
       # print("@@@@@@@@@@@@@@@@@@@")
       # print(len(picked))
       # for i in range(len(picked)):
       ##     print(i)
         #   print(picked[i])
         #   game = Game.objects.get(id = picked[i])
          #  print("@@@@@@@@@@@@@@@@@@@")
           # meet.games.add(game)                      
        
        meet.save()
        
        return getMeet(request, meet.id)
    
    return render(
        request,
        'catalog/meet_form.html',
        context = {
            'form' : form,
        },
    )

def getMeetsCurrent(request):

    meets = Meet.objects.filter(
    
        date__gte = datetime.datetime.today()
    
    )    
    
    for i in range(len(meets)):        
        meets[i].count = len(meets[i].users.all())
        
    return render(
        request,
        'adminp/meets_non.html',
        context = {
            'meets' : meets
        },
    )
    
def getMeetsHistory(request):

    meets = Meet.objects.filter(
    
        date__lt = datetime.datetime.today()
    
    )    
        
    return render(
        request,
        'adminp/meets_old.html',
        context = {
            'meets' : meets
        },
    )
    
def getMeet(request, pk):

    meet = Meet.objects.get(pk = pk)
    users = meet.users.all()       
    
    return render(
        request,
        'adminp/meet.html',
        context = {
            'meet' : meet,           
            'users' : users
        },
    )
    
def getGameAdmin(request, pk):

    game = Game.objects.get(pk = pk)
    images = Gallery.objects.filter(game = pk)
    
    return render(
        request,
        'adminp/game_view.html',
        context = {
            'game' : game,
            'images' : images,
        },
    )
    
def getGallery(request):
    
    gallery = Gallery.objects.all()
    
    return render(
        request,
        'adminp/gallery.html',
        context = {
            'gallery' : gallery,            
        },
    )
    
def getAuthors(request):
    
    authors = Author.objects.all()
    
    return render(
        request,
        'adminp/authors.html',
        context = {
            'authors' : authors,            
        },
    )
    
def getGenres(request):
    
    genres = Genre.objects.all()
    
    return render(
        request,
        'adminp/genres.html',
        context = {
            'genres' : genres,            
        },
    )
    
def toMeet(request, pk):

    is_auth = 2

    if request.user.is_authenticated:
        
        meet = Meet.objects.get(pk = pk)
                       
        try:
            user_is = meet.users.get(id = request.user.id)
            is_auth = 3
            meet.users.remove(user_is)
        except User.DoesNotExist:
            is_auth = 1            
            meet.users.add(request.user)

        meet.save()
           
    return getMeets(request, is_auth)
    
def getUsers(request):
    
    users = User.objects.filter(is_staff = False)
    
    return render(
        request,
        'adminp/users.html',
        context = {
            'users' : users,            
        },
    )
    
def setUserToStaff(request, pk):

    user = User.objects.get(pk = pk)
    user.is_staff = True
    user.customer.super_was = True
    user.customer.super_customer = True
    user.save()
    
    return getUsers(request)
    
def delFormGallery(request, pk):
    
    gallery = Gallery.objects.get(pk = pk)
    
    gallery.delete()
    
    return getGallery(request)
    
def getProfile(request):

    if request.method == 'POST':
        
        user = User.objects.get(id = request.user.id)        
        
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('mail')
        user.first_name = request.POST.get('first_name')
        
        user.save()
        
        return render(
            request,
            'catalog/profile_done.html',
            context = {

            },
        )
    
    checks = Check.objects.filter(user_id = request.user.id)
    
    return render(
        request,
        'catalog/profile.html',
        context = {
            'checks' : checks,
        },
    )
    
def UserDelete(request, pk):
    
    user = User.objects.get(pk = pk)
    user.customer.delete()
    user.delete()
    
    return getUsers(request)
    
class UserUpdate(UpdateView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('staff_shop')    
    
class CustomerUpdate(UpdateView):
    model = Customer
    fields = '__all__'
    success_url = reverse_lazy('staff_shop')
    
class GalleryUpdate(UpdateView):
    model = Gallery
    fields = '__all__'
    success_url = reverse_lazy('gallery')
    
class GenreCreate(CreateView):
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('game_add')
    
class GenreUpdate(UpdateView):
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('genres')

class GenreDelete(DeleteView):
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('genres')
    
### AUTHORS ###
    
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('game_add')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']
    success_url = reverse_lazy('authors')

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
