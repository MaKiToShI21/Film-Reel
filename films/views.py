from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound


def all_films(request):
    return HttpResponse(f"<h1>Страница со всеми фильмами</h1>")

def film_name(request, name):  
    return HttpResponse(f"<h1>Страница фильма: {name}</h1>")

def films_by_rating(request, film_rating):
    if film_rating >= 8.0:
        category = "Отличный фильм"
    elif film_rating >= 7.0:
        category = "Хороший фильм"
    elif film_rating >= 6.0:
        category = "Неплохой фильм"
    elif film_rating >= 5.0:
        category = "Средний фильм"
    else:
        category = "Слабый фильм"

    return HttpResponse(f"<h1>{category}<h1>")

def films_by_year(request, film_year):
    return HttpResponse(f"<h1>Фильмы {film_year} года</h1>")

def films_by_genre(request):
    genre = request.GET.get('genre', 'не указан')
    year = request.GET.get('year', 'не указан')
    return HttpResponse(f"<h1>Поиск фильмов</h1><p>Жанр: {genre}</p><p>Год: {year}</p>")

def old_films_redirect(request):
    return redirect('films:all_films')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404: Страница не найдена</h1><p>Проверьте правильность введённого адреса</p>")
