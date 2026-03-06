from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound


FILMS_DATA = [
    {'id': 1, 'title': 'Начало', 'year': 2010, 'rating': 7.8, 'genre': 'Фантастика', 'description': 'Фантастический боевик о снах во сне.'},
    {'id': 2, 'title': 'Зеленая книга', 'year': 2018, 'rating': 8.5, 'genre': 'Драма', 'description': 'История о дружбе музыканта и водителя.'},
    {'id': 3, 'title': '1+1', 'year': 2011, 'rating': 8.7, 'genre': 'Комедия', 'description': 'Французская комедия о парализованном аристократе.'},
    {'id': 4, 'title': 'Интерстеллар', 'year': 2014, 'rating': 8.6, 'genre': 'Фантастика', 'description': 'Путешествие через червоточину.'},
    {'id': 5, 'title': 'Криминальное чтиво', 'year': 1994, 'rating': 8.9, 'genre': 'Криминал', 'description': 'Криминальные истории Тарантино.'},
]

MENU = [
    {'title': 'Главная', 'url_name': 'homepage:homepage'},
    {'title': 'Все фильмы', 'url_name': 'films:index', 'args': ['all']},
    {'title': 'О проекте', 'url_name': 'films:about'},
]

def index(request, name):
    """Главная страница фильмов"""
    if name != 'all':
        films = [f for f in FILMS_DATA if f['genre'].lower() == name.lower()]
        title = f'Фильмы жанра: {name}'
    else:
        films = FILMS_DATA
        title = 'Все фильмы'

    context = {
        'title': title,
        'films': films,
        'menu': MENU,
    }
    return render(request, 'films/index.html', context)


def category(request, id):
    """Страница отдельного фильма"""
    film = None
    for f in FILMS_DATA:
        if f['id'] == id:
            film = f
            break

    if not film:
        return HttpResponseNotFound("<h1>Фильм не найден</h1>")

    context = {
        'title': film['title'],
        'film': film,
        'menu': MENU,
    }
    return render(request, 'films/film_detail.html', context)


def films_by_year(request, year):
    """Фильмы по году"""
    films = [f for f in FILMS_DATA if f['year'] == year]
    context = {
        'title': f'Фильмы {year} года',
        'films': films,
        'menu': MENU,
    }
    return render(request, 'films/index.html', context)


def films_by_rating(request, rating):
    """Фильмы по рейтингу"""
    films = [f for f in FILMS_DATA if f['rating'] >= rating]
    context = {
        'title': f'Фильмы с рейтингом от {rating}',
        'films': films,
        'menu': MENU,
    }
    return render(request, 'films/index.html', context)


def search(request):
    """Поиск фильмов"""
    query = request.GET.get('q', '')
    if query:
        films = [f for f in FILMS_DATA if query.lower() in f['title'].lower()]
    else:
        films = []

    context = {
        'title': f'Поиск: {query}' if query else 'Поиск фильмов',
        'films': films,
        'menu': MENU,
        'query': query,
    }
    return render(request, 'films/search.html', context)


def redirect_to_homepage(request):
    """Перенаправление на главную"""
    return redirect('homepage:homepage')


# def all_films(request):
#     return HttpResponse(f"<h1>Страница со всеми фильмами</h1>")

# def film_name(request, name):
#     return HttpResponse(f"<h1>Страница фильма: {name}</h1>")

# def films_by_rating(request, film_rating):
#     if film_rating >= 8.0:
#         category = "Отличный фильм"
#     elif film_rating >= 7.0:
#         category = "Хороший фильм"
#     elif film_rating >= 6.0:
#         category = "Неплохой фильм"
#     elif film_rating >= 5.0:
#         category = "Средний фильм"
#     else:
#         category = "Слабый фильм"

#     return HttpResponse(f"<h1>{category}<h1>")

# def films_by_year(request, film_year):
#     return HttpResponse(f"<h1>Фильмы {film_year} года</h1>")

# def films_by_genre(request):
#     genre = request.GET.get('genre', 'не указан')
#     year = request.GET.get('year', 'не указан')
#     return HttpResponse(f"<h1>Поиск фильмов</h1><p>Жанр: {genre}</p><p>Год: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404: Страница не найдена</h1><p>Проверьте правильность введённого адреса</p>")
