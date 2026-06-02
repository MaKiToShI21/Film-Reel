from django.db.models import Avg

from .models import FilmRating, Films


def get_rater_key(request):
    if request.user.is_authenticated:
        return f"user:{request.user.pk}"
    if not request.session.session_key:
        request.session.save()
    return f"session:{request.session.session_key}"


def get_user_film_rating(request, film):
    if not request.user.is_authenticated:
        return None
    rating = FilmRating.objects.filter(
        film_id=film.pk,
        rater_key=get_rater_key(request),
    ).first()
    return rating.score if rating else None


def recalculate_film_rating(film_pk):
    avg = (
        FilmRating.objects.filter(film_id=film_pk)
        .aggregate(avg=Avg("score"))
        .get("avg")
    )
    new_rating = round(avg, 1) if avg is not None else 0.0
    Films.objects.filter(pk=film_pk).update(rating=new_rating)
    return new_rating


def set_user_film_rating(film, rater_key, score):
    FilmRating.objects.update_or_create(
        film_id=film.pk,
        rater_key=rater_key,
        defaults={"score": score},
    )
    return recalculate_film_rating(film.pk)


def clear_user_film_rating(film, rater_key):
    FilmRating.objects.filter(film_id=film.pk, rater_key=rater_key).delete()
    return recalculate_film_rating(film.pk)
