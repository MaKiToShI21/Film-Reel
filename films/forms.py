from datetime import date
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Director, Films, TagPost


def validate_film_title(value):
    if not re.fullmatch(r"[A-Za-zА-Яа-яЁё0-9\s:\-!?,.()]+", value):
        raise ValidationError(
            "Название может содержать только буквы, цифры, пробелы и базовые знаки пунктуации."
        )


class AddFilmForm(forms.Form):
    title = forms.CharField(max_length=255, label="Название", validators=[validate_film_title])
    slug = forms.SlugField(max_length=255, label="URL")
    year = forms.IntegerField(
        min_value=1888,
        max_value=date.today().year + 1,
        label="Год выпуска",
    )
    rating = forms.FloatField(min_value=0, max_value=10, label="Рейтинг")
    genre = forms.CharField(max_length=100, label="Жанр")
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 50}),
        required=False,
        label="Описание",
    )
    is_published = forms.BooleanField(required=False, label="Опубликовано")
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категория не выбрана",
        label="Категория",
    )
    director = forms.ModelChoiceField(
        queryset=Director.objects.all(),
        required=False,
        empty_label="Режиссер не выбран",
        label="Режиссер",
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.all(),
        required=False,
        label="Теги",
    )


class AddFilmModelForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, label="Опубликовано")
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категория не выбрана",
        label="Категория",
    )
    director = forms.ModelChoiceField(
        queryset=Director.objects.all(),
        required=False,
        empty_label="Режиссер не выбран",
        label="Режиссер",
    )

    class Meta:
        model = Films
        fields = [
            "title",
            "slug",
            "year",
            "rating",
            "genre",
            "description",
            "poster",
            "is_published",
            "cat",
            "director",
            "tags",
        ]
        labels = {
            "slug": "URL",
            "poster": "Постер",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"rows": 5, "cols": 50}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина названия превышает 50 символов.")
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
