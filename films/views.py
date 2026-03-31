from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.db import models
from django.db.models import Count
from .models import Films, Category, TagPost


MENU = [
    {'title': 'Главная', 'url_name': 'homepage:index'},
    {'title': 'Все фильмы', 'url_name': 'films:index', 'args': ['all']},
    {'title': 'О проекте', 'url_name': 'homepage:about'},
]


def index(request, name):
    if name != 'all':
        films = Films.published.filter(genre__iexact=name)
        title = f'Фильмы жанра: {name}'
    else:
        films = Films.published.all()
        title = 'Все фильмы'

    categories = Category.objects.annotate(
        total_films=Count('films')
    ).filter(total_films__gt=0)

    context = {
        'title': title,
        'films': films,
        'menu': MENU,
        'categories': categories,
        'cat_selected': None,
    }
    return render(request, 'films/index.html', context)


def film_detail(request, film_slug):
    film = get_object_or_404(Films, slug=film_slug, is_published=Films.Status.PUBLISHED)

    context = {
        'title': film.title,
        'film': film,
        'menu': MENU,
    }
    return render(request, 'films/film_detail.html', context)


def films_by_year(request, film_year):
    films = Films.published.filter(year=film_year)
    categories = Category.objects.annotate(
        total_films=Count('films')
    ).filter(total_films__gt=0)

    context = {
        'title': f'Фильмы {film_year} года',
        'films': films,
        'menu': MENU,
        'categories': categories,
        'cat_selected': None,
    }
    return render(request, 'films/index.html', context)


def films_by_rating(request, film_rating):
    films = Films.published.filter(rating__gte=film_rating)
    categories = Category.objects.annotate(
        total_films=Count('films')
    ).filter(total_films__gt=0)

    context = {
        'title': f'Фильмы с рейтингом от {film_rating}',
        'films': films,
        'menu': MENU,
        'categories': categories,
        'cat_selected': None,
    }
    return render(request, 'films/index.html', context)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    films = Films.published.filter(cat_id=category.pk)
    categories = Category.objects.annotate(
        total_films=Count('films')
    ).filter(total_films__gt=0)

    context = {
        'title': f'Категория: {category.name}',
        'films': films,
        'menu': MENU,
        'categories': categories,
        'cat_selected': category.pk,
    }
    return render(request, 'films/index.html', context)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    films = tag.films.filter(is_published=Films.Status.PUBLISHED)
    categories = Category.objects.annotate(
        total_films=Count('films')
    ).filter(total_films__gt=0)

    context = {
        'title': f'Тег: {tag.tag}',
        'films': films,
        'menu': MENU,
        'categories': categories,
        'cat_selected': None,
    }
    return render(request, 'films/index.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404: Страница не найдена</h1><p>Проверьте правильность введённого адреса</p>")
