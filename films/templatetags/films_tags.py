from django import template
from films.views import FILMS_DATA

register = template.Library()

# Простой тег - возвращает список фильмов
@register.simple_tag
def get_all_films():
    """Возвращает все фильмы"""
    return FILMS_DATA

@register.simple_tag
def get_num_of_all_films():
    """Возвращает все фильмы"""
    return len(FILMS_DATA)

# Простой тег с параметром - возвращает фильмы по жанру
@register.simple_tag
def get_films_by_genre(genre):
    """Возвращает фильмы определенного жанра"""
    return [film for film in FILMS_DATA if film['genre'].lower() == genre.lower()]

# Включающий тег - отображает список фильмов
@register.inclusion_tag('films/film_list.html')
def show_films(films=None):
    """Отображает список фильмов"""
    if films is None:
        films = FILMS_DATA
    return {'films': films}

# Фильтр - форматирует рейтинг
@register.filter
def format_rating(rating):
    """Форматирует рейтинг"""
    if rating >= 8.5:
        return f"⭐ {rating} (Отлично)"
    elif rating >= 7.0:
        return f"⭐ {rating} (Хорошо)"
    else:
        return f"⭐ {rating}"
