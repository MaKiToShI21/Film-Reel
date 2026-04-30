from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter, RatingConverter

register_converter(FourDigitYearConverter, "four_year")
register_converter(RatingConverter, "rating")

app_name = "films"

urlpatterns = [
    path("", views.home, name="home"),
    path("film/<slug:film_slug>/", views.film_detail, name="film_detail"),
    path("year/<four_year:film_year>/", views.films_by_year, name="films_by_year"),
    path("rating/<rating:film_rating>/", views.films_by_rating, name="films_by_rating"),
    path("category/<slug:cat_slug>/", views.show_category, name="category"),
    path("tag/<slug:tag_slug>/", views.show_tag_postlist, name="tag"),
    path("add-form/", views.add_film_form, name="add_film_form"),
    path("add-model/", views.add_film_model, name="add_film_model"),
    path("upload-file/", views.upload_file, name="upload_file"),
    path("<slug:name>/", views.index, name="index"),
]
