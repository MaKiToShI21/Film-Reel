from django.db import migrations, models


DEFAULT_DURATION = 90


def fill_missing_film_data(apps, schema_editor):
    Films = apps.get_model("films", "Films")
    FilmDetails = apps.get_model("films", "FilmDetails")
    Genre = apps.get_model("films", "Genre")

    default_genre, _ = Genre.objects.get_or_create(name="Драма")

    for film in Films.objects.all():
        if not film.description:
            film.description = "Описание будет добавлено позже."
            film.save(update_fields=["description"])

        if not film.genres.exists():
            film.genres.add(default_genre)

        details, _ = FilmDetails.objects.get_or_create(
            film=film,
            defaults={"duration": DEFAULT_DURATION},
        )
        if details.duration is None:
            details.duration = DEFAULT_DURATION
            details.save(update_fields=["duration"])


class Migration(migrations.Migration):
    dependencies = [
        ("films", "0005_remove_category"),
    ]

    operations = [
        migrations.RunPython(fill_missing_film_data, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="films",
            name="description",
            field=models.TextField(verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="films",
            name="genres",
            field=models.ManyToManyField(
                related_name="films",
                to="films.genre",
                verbose_name="Жанры",
            ),
        ),
        migrations.AlterField(
            model_name="films",
            name="tags",
            field=models.ManyToManyField(
                related_name="films",
                to="films.tagpost",
                verbose_name="Теги",
            ),
        ),
        migrations.AlterField(
            model_name="filmdetails",
            name="duration",
            field=models.PositiveIntegerField(verbose_name="Длительность (мин)"),
        ),
    ]
