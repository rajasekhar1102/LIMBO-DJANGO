from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
# Register your models here.


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ['name',]
    ordering = ['name']
    search_fields = ['name']


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ['title', 'genre', 'numberInStock', 'dailyRentalRate']
    autocomplete_fields = ['genre']
    search_fields = ['title']


@admin.register(UserLikes)
class UserLikeAdmin(ModelAdmin):
    list_display = ['like', 'user', 'movie']
    autocomplete_fields = ['user', 'movie']
    ordering = ['user', 'movie', 'like']


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'date_of_birth', 'picture_tag', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']

    class Media:
        css = {
            'all': ['movie/styles.css']
        }
