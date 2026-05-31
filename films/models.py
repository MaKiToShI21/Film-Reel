from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


def upload_file_to(instance, filename):
    import os
    import uuid

    ext = os.path.splitext(filename)[1]
    return f"uploads_model/{uuid.uuid4()}{ext}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Films.Status.PUBLISHED)


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        db_table = "tags"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("films:tag", kwargs={"tag_slug": self.slug})


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Жанр")

    class Meta:
        db_table = "genres"
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя режиссера")
    age = models.IntegerField(null=True, blank=True, verbose_name="Возраст")
    bio = models.TextField(blank=True, verbose_name="Биография")
    oscars_count = models.IntegerField(default=0, verbose_name="Количество Оскаров")
    m_count = models.IntegerField(blank=True, default=0, verbose_name="Счетчик наград")

    class Meta:
        db_table = "directors"
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

    def __str__(self):
        return self.name


class Films(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
        verbose_name="URL",
    )
    year = models.IntegerField(verbose_name="Год выпуска")
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Рейтинг",
    )
    description = models.TextField(verbose_name="Описание")
    poster = models.ImageField(upload_to="films/", blank=True, null=True, verbose_name="Постер")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Опубликовано",
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="films",
        verbose_name="Жанры",
    )
    directors = models.ManyToManyField(
        Director,
        blank=True,
        related_name="films",
        verbose_name="Режиссёры",
    )
    tags = models.ManyToManyField(
        TagPost,
        related_name="films",
        verbose_name="Теги",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="films",
        null=True,
        default=None,
        verbose_name="Автор",
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        db_table = "films"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def get_absolute_url(self):
        return reverse("films:film_detail", kwargs={"film_slug": self.slug})

    def __str__(self):
        return self.title


class FilmRating(models.Model):
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="user_ratings",
        verbose_name="Фильм",
    )
    rater_key = models.CharField(max_length=150, db_index=True, verbose_name="Ключ оценившего")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка",
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        db_table = "film_ratings"
        constraints = [
            models.UniqueConstraint(
                fields=["film", "rater_key"],
                name="unique_film_rater",
            ),
        ]
        verbose_name = "Оценка фильма"
        verbose_name_plural = "Оценки фильмов"

    def __str__(self):
        return f"{self.film.title}: {self.score}"


class FilmDetails(models.Model):
    film = models.OneToOneField(
        Films,
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name="Фильм",
    )
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Бюджет ($)",
    )
    box_office = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Сборы ($)",
    )
    duration = models.PositiveIntegerField(verbose_name="Длительность (мин)")
    filming_location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Место съемок",
    )

    class Meta:
        db_table = "film_details"
        verbose_name = "Технические детали"
        verbose_name_plural = "Технические детали"

    def __str__(self):
        return f"Детали фильма: {self.film.title}"


class FilmComment(models.Model):
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Фильм",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
        verbose_name="Родительский комментарий",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="film_comments",
        verbose_name="Автор",
    )
    text = models.TextField(max_length=2000, verbose_name="Текст")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        db_table = "film_comments"
        ordering = ["time_create"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}"


class FilmCommentReaction(models.Model):
    LIKE = 1
    DISLIKE = -1

    comment = models.ForeignKey(
        FilmComment,
        on_delete=models.CASCADE,
        related_name="reactions",
        verbose_name="Комментарий",
    )
    reactor_key = models.CharField(max_length=150, db_index=True, verbose_name="Ключ реакции")
    value = models.SmallIntegerField(
        choices=((LIKE, "Нравится"), (DISLIKE, "Не нравится")),
        verbose_name="Реакция",
    )

    class Meta:
        db_table = "film_comment_reactions"
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "reactor_key"],
                name="unique_comment_reactor",
            ),
        ]
        verbose_name = "Реакция на комментарий"
        verbose_name_plural = "Реакции на комментарии"

    def __str__(self):
        return f"{self.comment_id}: {self.value}"
