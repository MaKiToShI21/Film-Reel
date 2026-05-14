from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter, RatingConverter

register_converter(FourDigitYearConverter, "four_year")
register_converter(RatingConverter, "rating")

app_name = "films"

urlpatterns = [
    path("", views.FilmsHome.as_view(), name="home"),
    path("about/", views.AboutCatalog.as_view(), name="about"),
    path(
        "film/<slug:film_slug>/",
        views.FilmDetail.as_view(),
        name="film_detail",
    ),
    path(
        "year/<four_year:film_year>/",
        views.FilmsByYear.as_view(),
        name="films_by_year",
    ),
    path(
        "rating/<rating:film_rating>/",
        views.FilmsByRating.as_view(),
        name="films_by_rating",
    ),
    path(
        "category/<slug:cat_slug>/",
        views.FilmsCategory.as_view(),
        name="category",
    ),
    path(
        "tag/<slug:tag_slug>/",
        views.FilmsTagList.as_view(),
        name="tag",
    ),
    path(
        "add-form/",
        views.AddFilmFormPage.as_view(),
        name="add_film_form",
    ),
    path(
        "add-model/",
        views.AddFilmModelPage.as_view(),
        name="add_film_model",
    ),
    path(
        "upload-file/",
        views.UploadFilePage.as_view(),
        name="upload_file",
    ),
    path(
        "edit/<int:pk>/",
        views.FilmUpdatePage.as_view(),
        name="film_edit",
    ),
    path(
        "delete/<int:pk>/",
        views.FilmDeletePage.as_view(),
        name="film_delete",
    ),
    path("<slug:name>/", views.FilmsByGenre.as_view(), name="index"),
]
