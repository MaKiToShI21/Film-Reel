from django.db import migrations, models


def migrate_categories_to_genres(apps, schema_editor):
    Films = apps.get_model("films", "Films")
    Category = apps.get_model("films", "Category")
    Genre = apps.get_model("films", "Genre")

    for film in Films.objects.all():
        for category in film.categories.all():
            genre, _ = Genre.objects.get_or_create(name=category.name)
            film.genres.add(genre)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0004_film_relations_refactor"),
    ]

    operations = [
        migrations.RunPython(migrate_categories_to_genres, noop_reverse),
        migrations.RemoveField(
            model_name="films",
            name="categories",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.AlterField(
            model_name="films",
            name="is_published",
            field=models.BooleanField(
                choices=[(False, "Черновик"), (True, "Опубликовано")],
                default=0,
                verbose_name="Опубликовано",
            ),
        ),
    ]
