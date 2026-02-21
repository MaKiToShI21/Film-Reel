from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter, RatingConverter

register_converter(FourDigitYearConverter, 'year4')
register_converter(RatingConverter, 'rating')

app_name = 'films'

urlpatterns = [
    path('', views.all_films, name='all_films'),
    path('year/<year4:film_year>/', views.films_by_year, name='films_by_year'),
    path('rating/<rating:film_rating>/', views.films_by_rating, name='films_by_rating'),
    path('search/', views.films_by_genre, name='search'),
    path('movies/', views.old_films_redirect, name='old_films'),
    path('<slug:name>/', views.film_name, name='film_name'),
]
