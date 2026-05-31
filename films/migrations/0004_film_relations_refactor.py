from django.db import migrations, models


def migrate_film_relations(apps, schema_editor):
    Films = apps.get_model("films", "Films")
    Genre = apps.get_model("films", "Genre")
    genre_cache = {}

    for film in Films.objects.all():
        genre_value = getattr(film, "genre", "")
        if genre_value:
            genre_name = genre_value.strip()
            if genre_name:
                cache_key = genre_name.lower()
                if cache_key not in genre_cache:
                    genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                    genre_cache[cache_key] = genre_obj
                film.genres.add(genre_cache[cache_key])

        cat_id = getattr(film, "cat_id", None)
        if cat_id:
            film.categories.add(cat_id)

        director_id = getattr(film, "director_id", None)
        if director_id:
            film.directors.add(director_id)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0003_capitalize_genres"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=100,
                        unique=True,
                        verbose_name="Жанр",
                    ),
                ),
            ],
            options={
                "verbose_name": "Жанр",
                "verbose_name_plural": "Жанры",
                "db_table": "genres",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="films",
            name="categories",
            field=models.ManyToManyField(
                blank=True,
                related_name="films",
                to="films.category",
                verbose_name="Категории",
            ),
        ),
        migrations.AddField(
            model_name="films",
            name="directors",
            field=models.ManyToManyField(
                blank=True,
                related_name="films",
                to="films.director",
                verbose_name="Режиссёры",
            ),
        ),
        migrations.AddField(
            model_name="films",
            name="genres",
            field=models.ManyToManyField(
                blank=True,
                related_name="films",
                to="films.genre",
                verbose_name="Жанры",
            ),
        ),
        migrations.AlterField(
            model_name="films",
            name="is_published",
            field=models.BooleanField(
                choices=[(False, "Черновик"), (True, "Опубликовано")],
                default=1,
                verbose_name="Опубликовано",
            ),
        ),
        migrations.AlterField(
            model_name="films",
            name="rating",
            field=models.FloatField(default=0, verbose_name="Рейтинг"),
        ),
        migrations.RunPython(migrate_film_relations, noop_reverse),
        migrations.RemoveField(
            model_name="films",
            name="cat",
        ),
        migrations.RemoveField(
            model_name="films",
            name="director",
        ),
        migrations.RemoveField(
            model_name="films",
            name="genre",
        ),
    ]
