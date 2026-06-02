from django.db import migrations


def _capitalize_genre(value):
    value = (value or "").strip()
    if not value:
        return value
    return value[0].upper() + value[1:].lower()


def capitalize_genres(apps, schema_editor):
    Films = apps.get_model("films", "Films")
    seen = {}
    for film in Films.objects.exclude(genre="").only("id", "genre"):
        new_genre = _capitalize_genre(film.genre)
        if new_genre != film.genre:
            Films.objects.filter(pk=film.pk).update(genre=new_genre)
        seen[new_genre] = seen.get(new_genre, 0) + 1


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(capitalize_genres, noop_reverse),
    ]
