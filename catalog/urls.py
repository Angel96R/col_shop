from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [

    path('', views.index, name='index-catalog'),
    
    url(r'^adminp/$', views.getAdmin, name='adminp'),
    
    url(r'^adminp/staff_shop/$', views.getStaffOfShop, name='staff_shop'),
    url(r'^adminp/staff_shop/remove_employee/(?P<pk>\d+)$', views.removeEmployee, name='staff_shop_remove'),
    url(r'^adminp/staff_shop/update/(?P<pk>\d+)$', views.UserUpdate.as_view(), name='staff_shop_update'),
    url(r'^adminp/staff_shop/access/(?P<pk>\d+)$', views.CustomerUpdate.as_view(), name='staff_shop_access'),
    
    url(r'^adminp/users/$', views.getUsers, name='users'),
    url(r'^adminp/users/delete/(?P<pk>\d+)$', views.UserDelete, name='user_delete'),
    url(r'^adminp/users/to_staff/(?P<pk>\d+)$', views.setUserToStaff, name='user_to_staff'),
    
    url(r'^adminp/carts_shop/$', views.getCartsOfShop, name='carts_shop'),
    url(r'^adminp/cart_shop/(?P<pk>\d+)$', views.getCartOfShop, name='cart_shop'),
    
    url(r'^adminp/games/$', views.getGamesToAdmin, name='adminp-games'),
    url(r'^adminp/games/del_game/(?P<pk>\d+)$', views.delGame, name='adminp-games-delete'),
    url(r'^adminp/games/edit_game/(?P<pk>\d+)$', views.GameUpdate.as_view(), name='game_update'),
    url(r'^adminp/games/add/$', views.GameCreate.as_view(), name='game_add'),
    url(r'^adminp/games/(?P<pk>\d+)$', views.getGameAdmin, name='game_view'),
    
    url(r'^adminp/gallery/$', views.getGallery, name='gallery'),    
    url(r'^adminp/gallery/delete/(?P<pk>\d+)$', views.delFormGallery, name='gallery_delete'),
    url(r'^adminp/games/gallery_game/create/$', views.GalleryCreate.as_view(), name='game_gallery_create'),
    url(r'^adminp/gallery/(?P<pk>\d+)$', views.GalleryUpdate.as_view(), name='gallery_update'),        

    url(r'^adminp/meets/add/$', views.MeetAdd, name='meets_add'),
    
    url(r'^adminp/authors/$', views.getAuthors, name='authors'),
    url(r'^adminp/author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^adminp/author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^adminp/author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    
    url(r'^adminp/genres/$', views.getGenres, name='genres'),
    url(r'^adminp/genre/create/$', views.GenreCreate.as_view(), name='genre_create'),
    url(r'^adminp/genre/(?P<pk>\d+)/update/$', views.GenreUpdate.as_view(), name='genre_update'),
    url(r'^adminp/genre/(?P<pk>\d+)/delete/$', views.GenreDelete.as_view(), name='genre_delete'),

    url(r'^adminp/check_create/$', views.CheckCreate.as_view(), name='checkout'),
    url(r'^adminp/check_sum/(?P<pk>\d+)$', csrf_exempt(views.sumCheck), name='check_sum'),
    url(r'^adminp/check_view/(?P<pk>\d+)$', csrf_exempt(views.checkViewAdmin), name='check_view_admin'),
    url(r'^adminp/check_non_comps/$', views.getChecksNonCompletes, name='checknoncomps'),
    url(r'^adminp/check_del/(?P<pk>\d+)$', views.delCheck, name='check_del'),
    url(r'^adminp/check_comp/(?P<pk>\d+)$', views.compCheck, name='check_complete'),
    url(r'^adminp/check_hist/$', views.getCheckHistory, name='checkhist'),        
    url(r'^adminp/check_report/$', views.getChecksReport, name='check_report'),        
    
    url(r'^adminp/meets_non/$', views.getMeetsCurrent, name='meets_current'),
    url(r'^adminp/meets_hist/$', views.getMeetsHistory, name='meets_hist'),
    url(r'^adminp/meet/(?P<pk>\d+)$', views.getMeet, name='meet_view'),    
    
    url(r'^games/$', views.getGames, name='games'),    
    url(r'^game/(?P<pk>\d+)$', views.getGame, name='game-detail'),          # WTF???
    
    url(r'^cart/$', views.getCart, name='cart'),
    url(r'^cart/item/del/(?P<pk>\d+)$', views.dellFromCart, name='cart_del_item'),
    url(r'^cart/item/add/(?P<pk>\d+)$', views.addToCart, name='cart_add_item'),
    
    url(r'^check/(?P<pk>\d+)$', views.getCheckToClient, name='check_view_client'),    
    
    url(r'^games/search/$', views.searchGame, name='game_search'),               
        
    url(r'^about/$', views.setAbout, name = 'about'),
    url(r'^about/edit/$', views.InfoSiteUpdate, name = 'about-edit'),
    
    url(r'^meets/$', views.getMeets, name = 'meets'),
    url(r'^meets/to/(?P<pk>\d+)$', views.toMeet, name = 'to_meet'),
    
    url(r'^register/$', views.RegisterFormView.as_view(), name = 'register'),    
    
    url(r'^profile/$', views.getProfile, name = 'profile'),    
]