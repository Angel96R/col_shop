from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [

    path('', views.index, name='index-catalog'),
    
    url(r'^games/$', views.getGames, name='games'),    
    url(r'^game/(?P<pk>\d+)$', views.getGame, name='game-detail'),          # WTF???
    
    url(r'^cart/$', views.getCart, name='cart'),
    url(r'^cart/item/del/(?P<pk>\d+)$', views.dellFromCart, name='cart_del_item'),
    url(r'^cart/item/add/(?P<pk>\d+)$', views.addToCart, name='cart_add_item'),
    
    url(r'^games/search/$', views.searchGame, name='game_search'),
    
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    
]