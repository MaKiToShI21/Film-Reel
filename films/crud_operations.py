import os
import sys
import django


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FilmReel.settings')
django.setup()

from django.db.models import F, Q, Count, Avg, Sum, Max, Min
from films.models import Films, Category, TagPost, Director, FilmDetails
from django.db import connection
from django.db.models.functions import Length, Upper


def demo_crud_operations():
    print("1. CREATE - Создание новых записей")

    print("\n--- Создание категорий ---")
    categories_data = [
        {'name': 'Боевик', 'slug': 'boevik'},
        {'name': 'Драма', 'slug': 'drama'},
        {'name': 'Комедия', 'slug': 'comedy'},
        {'name': 'Фантастика', 'slug': 'fantastika'},
        {'name': 'Криминал', 'slug': 'kriminal'},
        {'name': 'Триллер', 'slug': 'triller'},
    ]

    created_categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name']}
        )
        created_categories.append(category)
        if created:
            print(f"   ✓ Создана категория: {category.name}")

    action_cat = Category.objects.get(slug='boevik')
    drama_cat = Category.objects.get(slug='drama')
    comedy_cat = Category.objects.get(slug='comedy')
    fantasy_cat = Category.objects.get(slug='fantastika')
    crime_cat = Category.objects.get(slug='kriminal')

    print("\n--- Создание тегов ---")
    tags_data = [
        {'tag': 'Оскар', 'slug': 'oskar'},
        {'tag': 'Блокбастер', 'slug': 'blokbaster'},
        {'tag': 'Шедевр', 'slug': 'shedevr'},
        {'tag': 'Культовый', 'slug': 'kultoviy'},
        {'tag': 'Номинант Оскара', 'slug': 'nominant-oskara'},
        {'tag': 'Золотой глобус', 'slug': 'zolotoy-globus'},
        {'tag': 'Каннский фестиваль', 'slug': 'kannskiy-festival'},
    ]

    created_tags = []
    for tag_data in tags_data:
        tag, created = TagPost.objects.get_or_create(
            slug=tag_data['slug'],
            defaults={'tag': tag_data['tag']}
        )
        created_tags.append(tag)
        if created:
            print(f"   ✓ Создан тег: {tag.tag}")

    print("\n--- Создание режиссеров ---")
    directors_data = [
        {'name': 'Кристофер Нолан', 'age': 53, 'oscars_count': 2, 'bio': 'Британско-американский режиссер, известный по фильмам "Тёмный рыцарь", "Начало", "Интерстеллар"'},
        {'name': 'Квентин Тарантино', 'age': 60, 'oscars_count': 2, 'bio': 'Американский режиссер, сценарист, известный по фильмам "Криминальное чтиво", "Бесславные ублюдки"'},
        {'name': 'Мартин Скорсезе', 'age': 81, 'oscars_count': 1, 'bio': 'Американский режиссер, продюсер, сценарист, обладатель Оскара за фильм "Отступники"'},
        {'name': 'Дэвид Финчер', 'age': 61, 'oscars_count': 0, 'bio': 'Американский режиссер, известный по фильмам "Бойцовский клуб", "Социальная сеть"'},
        {'name': 'Дени Вильнев', 'age': 56, 'oscars_count': 0, 'bio': 'Канадский режиссер, известный по фильмам "Прибытие", "Дюна"'},
    ]

    created_directors = []
    for d_data in directors_data:
        director, created = Director.objects.get_or_create(
            name=d_data['name'],
            defaults={
                'age': d_data['age'],
                'oscars_count': d_data['oscars_count'],
                'bio': d_data['bio']
            }
        )
        created_directors.append(director)
        if created:
            print(f"   ✓ Создан режиссер: {director.name}")

    print("\n--- Создание фильмов ---")
    films_data = [
        {
            'title': 'Начало',
            'slug': 'nachalo',
            'year': 2010,
            'rating': 8.8,
            'genre': 'Фантастика',
            'description': 'Кобб - вор, крадущий идеи из снов. Он должен выполнить невозможное задание - внедрить идею в сознание человека.',
            'cat': fantasy_cat,
            'director': created_directors[0],
            'tags': [created_tags[0], created_tags[1], created_tags[2]],
            'details': {
                'budget': 160000000,
                'box_office': 829000000,
                'duration': 148,
                'filming_location': 'Лос-Анджелес, Париж, Токио, Лондон'
            }
        },
        {
            'title': 'Криминальное чтиво',
            'slug': 'kriminalnoe-chtivo',
            'year': 1994,
            'rating': 8.9,
            'genre': 'Криминал',
            'description': 'Две переплетающиеся истории киллеров, боксера и жены гангстера.',
            'cat': crime_cat,
            'director': created_directors[1],
            'tags': [created_tags[0], created_tags[2], created_tags[3]],
            'details': {
                'budget': 8500000,
                'box_office': 213000000,
                'duration': 154,
                'filming_location': 'Лос-Анджелес'
            }
        },
        {
            'title': 'Волк с Уолл-стрит',
            'slug': 'volk-s-uoll-strit',
            'year': 2013,
            'rating': 8.0,
            'genre': 'Драма',
            'description': 'История взлета и падения брокера Джордана Белфорта.',
            'cat': drama_cat,
            'director': created_directors[1],
            'tags': [created_tags[1], created_tags[2], created_tags[4]],
            'details': {
                'budget': 100000000,
                'box_office': 392000000,
                'duration': 180,
                'filming_location': 'Нью-Йорк'
            }
        },
        {
            'title': 'Отель Гранд Будапешт',
            'slug': 'otel-grand-budapesht',
            'year': 2014,
            'rating': 8.1,
            'genre': 'Комедия',
            'description': 'Приключения легендарного консьержа и его ученика в вымышленной европейской стране.',
            'cat': comedy_cat,
            'director': None,
            'tags': [created_tags[2], created_tags[3], created_tags[5]],
            'details': {
                'budget': 25000000,
                'box_office': 174000000,
                'duration': 100,
                'filming_location': 'Германия'
            }
        },
        {
            'title': 'Отступники',
            'slug': 'otstupniki',
            'year': 2006,
            'rating': 8.5,
            'genre': 'Криминал',
            'description': 'Коп под прикрытием и преступник-информатор пытаются вычислить друг друга.',
            'cat': action_cat,
            'director': created_directors[2],
            'tags': [created_tags[0], created_tags[1], created_tags[3], created_tags[4]],
            'details': {
                'budget': 90000000,
                'box_office': 289000000,
                'duration': 151,
                'filming_location': 'Бостон'
            }
        },
        {
            'title': 'Бойцовский клуб',
            'slug': 'boytsovskiy-klub',
            'year': 1999,
            'rating': 8.8,
            'genre': 'Триллер',
            'description': 'Офисный работник и торговец мылом создают подпольный клуб, который перерастает во что-то большее.',
            'cat': drama_cat,
            'director': created_directors[3],
            'tags': [created_tags[2], created_tags[3], created_tags[6]],
            'details': {
                'budget': 63000000,
                'box_office': 100000000,
                'duration': 139,
                'filming_location': 'Лос-Анджелес'
            }
        },
        {
            'title': 'Дюна',
            'slug': 'dyuna',
            'year': 2021,
            'rating': 8.0,
            'genre': 'Фантастика',
            'description': 'Молодой Пол Атрейдес должен защитить свою планету от жестоких врагов.',
            'cat': fantasy_cat,
            'director': created_directors[4],
            'tags': [created_tags[1], created_tags[4], created_tags[5]],
            'details': {
                'budget': 165000000,
                'box_office': 402000000,
                'duration': 155,
                'filming_location': 'Иордания, ОАЭ, Норвегия'
            }
        },
        {
            'title': 'Интерстеллар',
            'slug': 'interstellar',
            'year': 2014,
            'rating': 8.6,
            'genre': 'Фантастика',
            'description': 'Группа исследователей отправляется через червоточину в поисках нового дома для человечества.',
            'cat': fantasy_cat,
            'director': created_directors[0],
            'tags': [created_tags[0], created_tags[1], created_tags[2]],
            'details': {
                'budget': 165000000,
                'box_office': 677000000,
                'duration': 169,
                'filming_location': 'Канада, Исландия'
            }
        },
    ]

    created_films = []
    for f_data in films_data:
        film, created = Films.objects.get_or_create(
            slug=f_data['slug'],
            defaults={
                'title': f_data['title'],
                'year': f_data['year'],
                'rating': f_data['rating'],
                'genre': f_data['genre'],
                'description': f_data['description'],
                'cat': f_data['cat'],
                'director': f_data['director'],
                'is_published': Films.Status.PUBLISHED
            }
        )
        if created:
            film.tags.set(f_data['tags'])
            created_films.append(film)
            print(f"   ✓ Создан фильм: {film.title} (ID: {film.pk})")

            if f_data['details']:
                details, created_details = FilmDetails.objects.get_or_create(
                    film=film,
                    defaults=f_data['details']
                )
                if created_details:
                    print(f"     → Добавлены детали фильма (бюджет: ${details.budget:,.0f}, сборы: ${details.box_office:,.0f})")

    print(f"\n   Итого создано фильмов: {len(created_films)}")

    print("\n" + "="*60)
    print("2. READ - Чтение записей с демонстрацией связей")
    print("="*60)

    all_films = Films.objects.all()
    print(f"\n   Всего фильмов в БД: {all_films.count()}")

    if all_films.exists():
        film = Films.objects.first()
        print(f"\n--- Демонстрация связей на примере фильма: {film.title} ---")
        print(f"   ID: {film.pk}")
        print(f"   Название: {film.title}")
        if film.cat:
            print(f"   Категория (Many-to-One): {film.cat.name}")
        if film.director:
            print(f"   Режиссер (Many-to-One): {film.director.name}")
        print(f"   Теги (Many-to-Many): {', '.join([t.tag for t in film.tags.all()])}")
        if hasattr(film, 'details'):
            print(f"   Детали фильма (One-to-One):")
            print(f"     - Бюджет: ${film.details.budget:,.0f}")
            print(f"     - Сборы: ${film.details.box_office:,.0f}")
            print(f"     - Длительность: {film.details.duration} мин")

    print("3. FILTER - Фильтрация записей")

    action_films = Films.objects.filter(cat__name='Боевик')
    print(f"\n   Боевики: {[f.title for f in action_films]}")

    oskar_films = Films.objects.filter(tags__tag='Оскар')
    print(f"   Фильмы с тегом 'Оскар': {[f.title for f in oskar_films]}")

    nolan_films = Films.objects.filter(director__name='Кристофер Нолан')
    print(f"   Фильмы Кристофера Нолана: {[f.title for f in nolan_films]}")

    high_rated = Films.objects.filter(rating__gte=8.5)
    print(f"   Фильмы с рейтингом >= 8.5: {[f.title for f in high_rated]}")

    high_budget = Films.objects.filter(details__budget__gt=100000000)
    print(f"   Фильмы с бюджетом > $100M: {[f.title for f in high_budget]}")

    complex_filter = Films.objects.filter(
        Q(rating__gte=8.5) | Q(details__box_office__gt=500000000)
    )
    print(f"   Фильмы с рейтингом >= 8.5 ИЛИ сборами > $500M: {[f.title for f in complex_filter]}")

    print("4. SORT - Сортировка записей")

    sorted_by_rating_desc = Films.objects.all().order_by('-rating')
    print(f"\n   Топ-5 по рейтингу:")
    for i, f in enumerate(sorted_by_rating_desc[:5], 1):
        print(f"     {i}. {f.title} - {f.rating}")

    sorted_by_box_office = Films.objects.filter(details__isnull=False).order_by('-details__box_office')
    if sorted_by_box_office.exists():
        print(f"\n   Топ-3 по кассовым сборам:")
        for i, f in enumerate(sorted_by_box_office[:3], 1):
            print(f"     {i}. {f.title} - ${f.details.box_office:,.0f}")

    print("5. UPDATE - Изменение записей")

    try:
        film_to_update = Films.objects.get(title='Начало')
        old_rating = film_to_update.rating
        film_to_update.rating = 9.0
        film_to_update.save()
        print(f"\n   Обновлен рейтинг фильма 'Начало': {old_rating:.1f} -> {film_to_update.rating:.1f}")
    except Films.DoesNotExist:
        print("\n   Фильм 'Начало' не найден")

    updated_count = Films.objects.filter(genre='Криминал').update(rating=F('rating') + 0.1)
    print(f"   Обновлено фильмов жанра 'Криминал': {updated_count}")

    all_films = Films.objects.all()
    for film in all_films:
        film.rating = round(film.rating, 1)
        film.save()
    print(f"   Все рейтинги округлены до 1 знака после запятой")

    try:
        nolan = Director.objects.get(name='Кристофер Нолан')
        old_oscars = nolan.oscars_count
        nolan.oscars_count = F('oscars_count') + 1
        nolan.save()
        nolan.refresh_from_db()
        print(f"   Обновлен счетчик Оскаров для {nolan.name}: {old_oscars} -> {nolan.oscars_count}")
    except Director.DoesNotExist:
        print("   Режиссер 'Кристофер Нолан' не найден")

    try:
        film = Films.objects.get(title='Интерстеллар')
        if hasattr(film, 'details'):
            old_box_office = film.details.box_office
            film.details.box_office = 700000000
            film.details.save()
            print(f"   Обновлены сборы фильма '{film.title}': ${old_box_office:,.0f} -> ${film.details.box_office:,.0f}")
    except Exception as e:
        print(f"   Ошибка при обновлении: {e}")

    print("\n" + "="*60)
    print("6. DELETE - Удаление записей")
    print("="*60)

    try:
        temp_film = Films.objects.create(
            title='Временный фильм',
            slug='vremennyy-film',
            year=2024,
            rating=5.0,
            genre='Тест',
            description='Временная запись для удаления',
            cat=comedy_cat,
            is_published=Films.Status.DRAFT
        )
        print(f"\n   Создан временный фильм: {temp_film.title}")
        temp_film.delete()
        print(f"   Удален временный фильм: {temp_film.title}")
    except Exception as e:
        print(f"\n   Ошибка при создании/удалении: {e}")

    print("\n" + "="*60)
    print("7. АГРЕГАЦИЯ - Статистические данные")
    print("="*60)

    film_stats = Films.objects.aggregate(
        avg_rating=Avg('rating'),
        max_rating=Max('rating'),
        min_rating=Min('rating'),
        total_films=Count('id'),
        total_published=Count('id', filter=Q(is_published=Films.Status.PUBLISHED))
    )
    print(f"\n   Статистика по фильмам:")
    print(f"     Средний рейтинг: {film_stats['avg_rating']:.2f}" if film_stats['avg_rating'] else "     Средний рейтинг: Нет данных")
    print(f"     Максимальный рейтинг: {film_stats['max_rating']}" if film_stats['max_rating'] else "     Максимальный рейтинг: Нет данных")
    print(f"     Минимальный рейтинг: {film_stats['min_rating']}" if film_stats['min_rating'] else "     Минимальный рейтинг: Нет данных")
    print(f"     Всего фильмов: {film_stats['total_films']}")
    print(f"     Опубликовано: {film_stats['total_published']}")

    financial_stats = FilmDetails.objects.aggregate(
        avg_budget=Avg('budget'),
        total_box_office=Sum('box_office'),
        avg_box_office=Avg('box_office'),
        max_box_office=Max('box_office')
    )
    print(f"\n   Финансовая статистика:")
    if financial_stats['avg_budget']:
        print(f"     Средний бюджет: ${financial_stats['avg_budget']:,.0f}")
    else:
        print("     Средний бюджет: Нет данных")

    if financial_stats['total_box_office']:
        print(f"     Общие сборы: ${financial_stats['total_box_office']:,.0f}")
    else:
        print("     Общие сборы: Нет данных")

    if financial_stats['avg_box_office']:
        print(f"     Средние сборы: ${financial_stats['avg_box_office']:,.0f}")
    else:
        print("     Средние сборы: Нет данных")

    if financial_stats['max_box_office']:
        print(f"     Максимальные сборы: ${financial_stats['max_box_office']:,.0f}")
    else:
        print("     Максимальные сборы: Нет данных")

    director_stats = Director.objects.aggregate(
        total_directors=Count('id'),
        avg_age=Avg('age'),
        total_oscars=Sum('oscars_count')
    )
    print(f"\n   Статистика по режиссерам:")
    print(f"     Всего режиссеров: {director_stats['total_directors']}")
    print(f"     Средний возраст: {director_stats['avg_age']:.1f} лет" if director_stats['avg_age'] else "     Средний возраст: Нет данных")
    print(f"     Всего Оскаров: {director_stats['total_oscars']}")

    print("\n" + "="*60)
    print("8. ГРУППИРОВКА - Статистика по группам")
    print("="*60)

    print("\n   Количество фильмов по категориям:")
    categories_stats = Category.objects.annotate(
        total_films=Count('films'),
        avg_rating=Avg('films__rating')
    ).filter(total_films__gt=0).order_by('-total_films')
    for cat in categories_stats:
        print(f"     {cat.name}: {cat.total_films} фильмов, средний рейтинг: {cat.avg_rating:.2f}")

    print("\n   Статистика по жанрам:")
    genres_stats = Films.objects.values('genre').annotate(
        count=Count('id'),
        avg_rating=Avg('rating'),
        max_rating=Max('rating')
    ).order_by('-count')
    for genre in genres_stats:
        print(f"     {genre['genre']}: {genre['count']} фильмов, средний рейтинг: {genre['avg_rating']:.2f}")

    print("\n   Статистика по годам:")
    years_stats = Films.objects.values('year').annotate(
        count=Count('id'),
        avg_rating=Avg('rating')
    ).order_by('-year')[:5]
    for year in years_stats:
        print(f"     {year['year']} год: {year['count']} фильмов, средний рейтинг: {year['avg_rating']:.2f}")

    print("9. ВЫЧИСЛЕНИЯ НА СТОРОНЕ СУБД")

    print("\n   Фильмы с длиной названия:")
    films_with_length = Films.objects.annotate(
        title_length=Length('title')
    ).order_by('-title_length').values('title', 'title_length')[:5]
    for f in films_with_length:
        print(f"     '{f['title']}': {f['title_length']} символов")

    print("\n   Названия фильмов в верхнем регистре:")
    films_upper = Films.objects.annotate(
        title_upper=Upper('title')
    ).values('title', 'title_upper')[:5]
    for f in films_upper:
        print(f"     {f['title']} -> {f['title_upper']}")

    long_titles = Films.objects.annotate(
        title_length=Length('title')
    ).filter(title_length__gt=15).values('title', 'title_length')
    print(f"\n   Фильмы с названием длиннее 15 символов: {long_titles.count()}")
    for f in long_titles[:5]:
        print(f"     '{f['title']}': {f['title_length']} символов")


if __name__ == "__main__":
    demo_crud_operations()
