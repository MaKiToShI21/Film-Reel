from django.urls import path, register_converter
from . import views
from .converters import FourDigitYearConverter, RatingConverter

register_converter(FourDigitYearConverter, 'four_year')
register_converter(RatingConverter, 'rating')

app_name = 'films'

urlpatterns = [
    path('film/<slug:film_slug>/', views.film_detail, name='film_detail'),
    path('year/<four_year:film_year>/', views.films_by_year, name='films_by_year'),
    path('rating/<rating:film_rating>/', views.films_by_rating, name='films_by_rating'),
    path('<slug:name>/', views.index, name='index'),
]
