from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0006_required_film_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="FilmRating",
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
                    "rater_key",
                    models.CharField(
                        db_index=True,
                        max_length=150,
                        verbose_name="Ключ оценившего",
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                        verbose_name="Оценка",
                    ),
                ),
                (
                    "time_create",
                    models.DateTimeField(auto_now_add=True, verbose_name="Время создания"),
                ),
                (
                    "time_update",
                    models.DateTimeField(auto_now=True, verbose_name="Время обновления"),
                ),
                (
                    "film",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_ratings",
                        to="films.films",
                        verbose_name="Фильм",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оценка фильма",
                "verbose_name_plural": "Оценки фильмов",
                "db_table": "film_ratings",
            },
        ),
        migrations.AddConstraint(
            model_name="filmrating",
            constraint=models.UniqueConstraint(
                fields=("film", "rater_key"),
                name="unique_film_rater",
            ),
        ),
    ]
