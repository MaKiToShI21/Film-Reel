from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """Менеджер для получения только опубликованных фильмов"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Films.Status.PUBLISHED)


class Films(models.Model):
    """Модель фильма"""
    
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    year = models.IntegerField(verbose_name="Год выпуска")
    rating = models.FloatField(verbose_name="Рейтинг")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    description = models.TextField(blank=True, verbose_name="Описание")
    poster = models.ImageField(upload_to='films/', blank=True, null=True, verbose_name="Постер")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Опубликовано")
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        db_table = 'films'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
    
    def get_absolute_url(self):
        return reverse('films:film_detail', kwargs={'film_slug': self.slug})
    
    def __str__(self):
        return self.title