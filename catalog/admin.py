from django.contrib import admin
from .models import Author, Genre, Game, Customer, Cart

#admin.site.register(Game)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Customer)
admin.site.register(Cart)

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin) # wtf???

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('title', 'author')
