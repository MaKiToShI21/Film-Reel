import os
import sys
import django

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FilmReel.settings')
django.setup()

from django.db.models import Q, F, Value, Count, Avg, Max, Min, Sum, CharField
from django.db.models.functions import Length, Upper
from films.models import Films, Category, TagPost, Director


def demo_advanced_orm():
    """Демонстрация продвинутых методов ORM"""

    print("1. Класс Q (сложные условия)")

    print("\nФильмы с рейтингом >= 8.5 ИЛИ жанром 'Комедия':")
    q_high_rated_or_comedy = Films.objects.filter(
        Q(rating__gte=8.5) | Q(genre__iexact='Комедия')
    )
    for film in q_high_rated_or_comedy[:5]:
        print(f"  - {film.title} (рейтинг: {film.rating}, жанр: {film.genre})")

    print("\nФильмы с рейтингом > 7.0 И (жанр 'Драма' ИЛИ год >= 2010):")
    complex_query = Films.objects.filter(
        Q(rating__gt=7.0) & (Q(genre='Драма') | Q(year__gte=2010))
    )
    for film in complex_query[:5]:
        print(f"  - {film.title} (рейтинг: {film.rating}, год: {film.year}, жанр: {film.genre})")

    print("2. Класс F (операции на уровне БД)")

    print("\nУвеличение счетчика Оскаров на 1 для всех режиссеров:")
    before_count = Director.objects.aggregate(total=Sum('oscars_count'))['total']
    if before_count is None:
        before_count = 0

    updated = Director.objects.update(oscars_count=F('oscars_count') + 1)
    after_count = Director.objects.aggregate(total=Sum('oscars_count'))['total']
    print(f"  Обновлено режиссеров: {updated}")
    print(f"  Общее количество Оскаров: {before_count} -> {after_count}")

    print("\nФильмы, у которых рейтинг выше года выпуска (условно):")
    rating_gt_year = Films.objects.filter(rating__gt=F('year') / 100)
    for film in rating_gt_year[:3]:
        print(f"  - {film.title}: рейтинг {film.rating} > год {film.year}/100 = {film.year/100:.1f}")

    print("3. Класс Value (константные поля)")

    print("\nРежиссеры с добавленными константными полями:")
    directors_with_const = Director.objects.annotate(
        is_active=Value(True, output_field=CharField()),
        status=Value("Активный", output_field=CharField())
    ).values('name', 'is_active', 'status')[:3]
    for d in directors_with_const:
        print(f"  - {d['name']}: активен? {d['is_active']}, статус: {d['status']}")

    print("4. Вычисляемые поля (annotate)")

    print("\nРежиссеры с вычисляемым стажем работы (возраст - 20):")
    directors_with_exp = Director.objects.annotate(
        experience=F('age') - 20
    ).exclude(experience__isnull=True).values('name', 'age', 'experience')[:3]
    for d in directors_with_exp:
        print(f"  - {d['name']}: возраст {d['age']}, стаж {d['experience']} лет")

    print("\nФильмы с длиной названия:")
    films_with_length = Films.objects.annotate(
        title_length=Length('title')
    ).values('title', 'title_length')[:5]
    for f in films_with_length:
        print(f"  - '{f['title']}': {f['title_length']} символов")

    print("5. Агрегирующие функции")

    print("\nСтатистика по фильмам:")
    film_stats = Films.objects.aggregate(
        avg_rating=Avg('rating'),
        max_rating=Max('rating'),
        min_rating=Min('rating'),
        total_films=Count('id'),
        total_published=Count('id', filter=Q(is_published=Films.Status.PUBLISHED))
    )
    print(f"  Средний рейтинг: {film_stats['avg_rating']:.2f}" if film_stats['avg_rating'] else "  Средний рейтинг: Нет данных")
    print(f"  Максимальный рейтинг: {film_stats['max_rating']}" if film_stats['max_rating'] else "  Максимальный рейтинг: Нет данных")
    print(f"  Минимальный рейтинг: {film_stats['min_rating']}" if film_stats['min_rating'] else "  Минимальный рейтинг: Нет данных")
    print(f"  Всего фильмов: {film_stats['total_films']}")
    print(f"  Опубликовано: {film_stats['total_published']}")

    print("\nСтатистика по режиссерам:")
    director_stats = Director.objects.aggregate(
        avg_age=Avg('age'),
        max_age=Max('age'),
        total_oscars=Sum('oscars_count')
    )
    print(f"  Средний возраст: {director_stats['avg_age']:.1f} лет" if director_stats['avg_age'] else "  Средний возраст: Нет данных")
    print(f"  Максимальный возраст: {director_stats['max_age']}" if director_stats['max_age'] else "  Максимальный возраст: Нет данных")
    print(f"  Всего Оскаров: {director_stats['total_oscars']}" if director_stats['total_oscars'] else "  Всего Оскаров: 0")

    print("6. Группировка записей")

    print("\nКоличество фильмов по категориям:")
    categories_stats = Category.objects.annotate(
        total_films=Count('films'),
        avg_rating=Avg('films__rating')
    ).values('name', 'total_films', 'avg_rating')
    for cat in categories_stats:
        avg = cat['avg_rating'] if cat['avg_rating'] else 0
        print(f"  - {cat['name']}: {cat['total_films']} фильмов, средний рейтинг: {avg:.2f}")

    print("\nСтатистика по жанрам:")
    genres_stats = Films.objects.values('genre').annotate(
        count=Count('id'),
        avg_rating=Avg('rating'),
        max_rating=Max('rating')
    ).order_by('-count')[:5]
    for genre in genres_stats:
        print(f"  - {genre['genre']}: {genre['count']} фильмов, средний рейтинг: {genre['avg_rating']:.2f}")

    print("\nСтатистика по годам:")
    years_stats = Films.objects.values('year').annotate(
        count=Count('id'),
        avg_rating=Avg('rating')
    ).order_by('-year')[:5]
    for year in years_stats:
        print(f"  - {year['year']} год: {year['count']} фильмов, средний рейтинг: {year['avg_rating']:.2f}")

    print("7. Вычисления на стороне СУБД")

    print("\nФильмы, отсортированные по длине названия:")
    films_by_name_length = Films.objects.annotate(
        title_length=Length('title')
    ).order_by('-title_length').values('title', 'title_length')[:5]
    for f in films_by_name_length:
        print(f"  - '{f['title']}': {f['title_length']} символов")

    print("\nНазвания фильмов в верхнем регистре:")
    films_upper = Films.objects.annotate(
        title_upper=Upper('title')
    ).values('title', 'title_upper')[:3]
    for f in films_upper:
        print(f"  - {f['title']} -> {f['title_upper']}")

    print("\nФильмы с названием длиннее 15 символов:")
    long_titles = Films.objects.annotate(
        title_length=Length('title')
    ).filter(title_length__gt=15).values('title', 'title_length')
    for f in long_titles:
        print(f"  - '{f['title']}': {f['title_length']} символов")


if __name__ == "__main__":
    demo_advanced_orm()
