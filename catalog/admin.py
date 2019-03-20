from django.contrib import admin
from .models import Author, Genre, Game

#admin.site.register(Game)
#admin.site.register(Author)
admin.site.register(Genre)

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('title', 'author')
