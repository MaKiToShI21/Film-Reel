from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter, RatingConverter, UnicodeSlugConverter

register_converter(FourDigitYearConverter, "four_year")
register_converter(RatingConverter, "rating")
register_converter(UnicodeSlugConverter, "uslug")

app_name = "films"

urlpatterns = [
    path("", views.FilmsHome.as_view(), name="home"),
    path("about/", views.AboutCatalog.as_view(), name="about"),
    path(
        "film/<uslug:film_slug>/",
        views.FilmDetail.as_view(),
        name="film_detail",
    ),
    path(
        "film/<uslug:film_slug>/rate/",
        views.rate_film,
        name="film_rate",
    ),
    path(
        "film/<uslug:film_slug>/comments/",
        views.post_film_comment,
        name="film_comment_post",
    ),
    path(
        "film/<uslug:film_slug>/comments/<int:comment_id>/edit/",
        views.edit_film_comment,
        name="film_comment_edit",
    ),
    path(
        "film/<uslug:film_slug>/comments/<int:comment_id>/delete/",
        views.delete_film_comment,
        name="film_comment_delete",
    ),
    path(
        "film/<uslug:film_slug>/comments/<int:comment_id>/vote/",
        views.vote_film_comment,
        name="film_comment_vote",
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
        "my-films/",
        views.MyFilms.as_view(),
        name="my_films",
    ),
    path(
        "edit/<uslug:name>/",
        views.FilmUpdatePage.as_view(),
        name="film_edit",
    ),
    path(
        "delete/<uslug:name>/",
        views.FilmDeletePage.as_view(),
        name="film_delete",
    ),
    path("<slug:name>/", views.FilmsByGenre.as_view(), name="index"),
]
