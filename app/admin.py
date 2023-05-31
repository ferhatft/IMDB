from django.contrib import admin
from .models import Movie, TVShow, Actor

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('actors',)
    search_fields = ['title', 'director']

admin.site.register(Movie, MovieAdmin)

class TVShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('actors',)
    search_fields = ['title', 'director']

admin.site.register(TVShow, TVShowAdmin)

admin.site.register(Actor)
