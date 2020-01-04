from django.contrib import admin
from .models import Author, Genre, Game, Customer, Cart, City, Shops, Gallery, Check, InfoSite, Meet

#admin.site.register(Game)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(City)
admin.site.register(Shops)
admin.site.register(Gallery)
admin.site.register(Check)
admin.site.register(InfoSite)
admin.site.register(Meet)
class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin) # wtf???

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('title', 'author')
