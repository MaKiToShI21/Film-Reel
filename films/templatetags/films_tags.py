from django import template
from films.models import Films

register = template.Library()


@register.simple_tag
def get_all_films():
    return Films.objects.all()


@register.simple_tag
def get_num_of_all_films():
    return Films.objects.count()


@register.simple_tag
def get_num_of_published_films():
    return Films.published.count()


@register.simple_tag
def get_films_by_genre(genre):
    return Films.published.filter(genre__iexact=genre)


@register.simple_tag
def get_films_by_min_rating(min_rating):
    return Films.published.filter(rating__gte=min_rating)


@register.inclusion_tag('films/film_list.html')
def show_films(films=None, limit=None):
    if films is None:
        films = Films.published.all()

    if limit:
        films = films[:limit]

    return {'films': films}


@register.filter
def format_rating(rating):
    if rating >= 8.5:
        return f"⭐ {rating} (Отлично)"
    elif rating >= 7.0:
        return f"⭐ {rating} (Хорошо)"
    elif rating >= 6.0:
        return f"⭐ {rating} (Неплохо)"
    elif rating >= 5.0:
        return f"⭐ {rating} (Средне)"
    else:
        return f"⭐ {rating} (Слабый)"


@register.filter
def rating_stars(rating):
    full_stars = int(rating // 1)
    half_star = rating % 1 >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)

    stars = '★' * full_stars
    if half_star:
        stars += '½'
    stars += '☆' * empty_stars

    return stars
