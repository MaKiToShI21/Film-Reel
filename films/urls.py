from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter, RatingConverter

register_converter(FourDigitYearConverter, 'four_year')
register_converter(RatingConverter, 'rating')

app_name = 'films'

urlpatterns = [
    path('<int:id>/', views.category, name='category'),
    path('year/<four_year:film_year>/', views.films_by_year, name='films_by_year'),
    path('rating/<rating:film_rating>/', views.films_by_rating, name='films_by_rating'),
    # path('search/', views.films_by_genre, name='search'),
    path('redirect-to-homepage/', views.redirect_to_homepage, name='redirect_to_homepage'),
    path('<slug:name>/', views.index, name='index'),
]
