import os
import sys
import django

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FilmReel.settings')
django.setup()

from films.models import Films
from django.db import connection


def demo_crud_operations():
    print("1. CREATE - Создание новой записи:")
    new_film = Films.objects.create(
        title='Джон Уик',
        slug='john-wick',
        year=2014,
        rating=7.4,
        genre='Боевик',
        description='Бывший наемный убийца выходит на тропу войны',
        is_published=Films.Status.PUBLISHED
    )
    print(f"   Создан фильм: {new_film.title} (ID: {new_film.pk})")

    print("\n2. READ - Чтение записей:")

    all_films = Films.objects.all()
    print(f"   Всего фильмов в БД: {all_films.count()}")

    film = Films.objects.get(pk=1)
    print(f"   Фильм с ID=1: {film.title}")

    print("\n3. FILTER - Фильтрация записей:")

    fantasy_films = Films.objects.filter(genre='Фантастика')
    print(f"   Фантастика: {[f.title for f in fantasy_films]}")

    high_rated = Films.objects.filter(rating__gte=8.5)
    print(f"   Фильмы с рейтингом >= 8.5: {[f.title for f in high_rated]}")

    recent_films = Films.objects.filter(year__gte=2010)
    print(f"   Фильмы после 2010 года: {[f.title for f in recent_films]}")

    not_drama = Films.objects.exclude(genre='Драма')
    print(f"   Фильмы не драма: {[f.title for f in not_drama]}")

    print("\n4. SORT - Сортировка записей:")

    sorted_by_rating_asc = Films.objects.all().order_by('rating')
    print(f"   По рейтингу (возрастание): {[(f.title, f.rating) for f in sorted_by_rating_asc[:3]]}")

    sorted_by_rating_desc = Films.objects.all().order_by('-rating')
    print(f"   По рейтингу (убывание): {[(f.title, f.rating) for f in sorted_by_rating_desc[:3]]}")

    sorted_by_year = Films.objects.all().order_by('-year')
    print(f"   По году (новые сначала): {[(f.title, f.year) for f in sorted_by_year[:3]]}")

    print("\n5. UPDATE - Изменение записей:")

    film_to_update = Films.objects.get(title='Джон Уик')
    film_to_update.rating = 7.6
    film_to_update.save()
    print(f"   Обновлен рейтинг фильма 'Джон Уик': {film_to_update.rating}")

    updated_count = Films.objects.filter(genre='Фантастика').update(rating=9.0)
    print(f"   Обновлено фильмов жанра 'Фантастика': {updated_count}")

    print("\n6. DELETE - Удаление записей:")

    film_to_delete = Films.objects.filter(title='Джон Уик').first()
    if film_to_delete:
        film_to_delete.delete()
        print(f"   Удален фильм: {film_to_delete.title}")


def show_sql_queries():
    queries = connection.queries
    if queries:
        print("\n=== ПОСЛЕДНИЕ SQL ЗАПРОСЫ ===")
        for i, query in enumerate(queries[-5:], 1):
            print(f"{i}. {query['sql']}")
            print(f"   Время: {query['time']}\n")

if __name__ == "__main__":
    demo_crud_operations()
    show_sql_queries()
