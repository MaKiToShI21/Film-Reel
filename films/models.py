import os
import uuid

from django.db import models
from django.urls import reverse


def upload_file_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads_model/{uuid.uuid4()}{ext}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Films.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("films:category", kwargs={"cat_slug": self.slug})


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
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    year = models.IntegerField(verbose_name="Год выпуска")
    rating = models.FloatField(verbose_name="Рейтинг")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    description = models.TextField(blank=True, verbose_name="Описание")
    poster = models.ImageField(upload_to="films/", blank=True, null=True, verbose_name="Постер")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Опубликовано",
    )
    cat = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="films",
        verbose_name="Категория",
        null=True,
    )
    tags = models.ManyToManyField(
        TagPost,
        blank=True,
        related_name="films",
        verbose_name="Теги",
    )
    director = models.ForeignKey(
        Director,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="films",
        verbose_name="Режиссер",
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
        verbose_name="Бюджет ($)",
    )
    box_office = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Сборы ($)",
    )
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name="Длительность (мин)")
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


class UploadFiles(models.Model):
    file = models.FileField(upload_to=upload_file_to, verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружен")

    class Meta:
        db_table = "upload_files"
        verbose_name = "Загруженный файл"
        verbose_name_plural = "Загруженные файлы"

    def __str__(self):
        return os.path.basename(self.file.name)
