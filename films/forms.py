from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from FilmReel.file_utils import delete_replaced_or_cleared_file

from .models import Director, FilmDetails, Films, Genre, TagPost

PICKER_WIDGET = forms.CheckboxSelectMultiple(
    attrs={"class": "film-form-picker-input"},
)

NON_NEGATIVE_NUMBER_ATTRS = {
    "class": "film-form-input",
    "min": "0",
    "step": "0.01",
}


class FilmPosterWidget(forms.ClearableFileInput):
    template_name = "films/clearable_poster_input.html"
    clear_checkbox_label = "Очистить"
    initial_text = "На данный момент:"
    input_text = "Изменить"


CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def transliterate_to_latin(text):
    return "".join(CYRILLIC_TO_LATIN.get(char, char) for char in text.lower())


def generate_unique_slug(title, instance_pk=None):
    latin_title = transliterate_to_latin(title)
    base = slugify(latin_title, allow_unicode=False) or "film"
    slug = base
    counter = 1
    while True:
        queryset = Films.objects.filter(slug=slug)
        if instance_pk:
            queryset = queryset.exclude(pk=instance_pk)
        if not queryset.exists():
            return slug
        counter += 1
        slug = f"{base}-{counter}"


class AddFilmModelForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.order_by("name"),
        label="Жанры",
        widget=PICKER_WIDGET,
    )
    directors = forms.ModelMultipleChoiceField(
        queryset=Director.objects.order_by("name"),
        required=False,
        label="Режиссёры",
        widget=PICKER_WIDGET,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.order_by("tag"),
        label="Теги",
        widget=PICKER_WIDGET,
    )
    budget = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
        label="Бюджет ($)",
        widget=forms.NumberInput(attrs=NON_NEGATIVE_NUMBER_ATTRS),
    )
    box_office = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
        label="Сборы ($)",
        widget=forms.NumberInput(attrs=NON_NEGATIVE_NUMBER_ATTRS),
    )
    duration = forms.IntegerField(
        min_value=1,
        label="Длительность (мин)",
        widget=forms.NumberInput(
            attrs={"class": "film-form-input", "min": "1", "step": "1"},
        ),
    )
    filming_location = forms.CharField(
        max_length=200,
        required=False,
        label="Место съёмок",
        widget=forms.TextInput(attrs={"class": "film-form-input"}),
    )

    class Meta:
        model = Films
        fields = [
            "title",
            "year",
            "description",
            "poster",
        ]
        labels = {
            "poster": "Постер",
            "year": "Год выпуска",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "film-form-input"}),
            "year": forms.TextInput(
                attrs={
                    "class": "film-form-input",
                    "inputmode": "numeric",
                    "maxlength": "4",
                    "pattern": r"\d{4}",
                    "placeholder": str(date.today().year),
                }
            ),
            "description": forms.Textarea(attrs={"rows": 5, "class": "film-form-input"}),
            "poster": FilmPosterWidget(attrs={"class": "film-form-file-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["genres"].initial = self.instance.genres.all()
            self.fields["directors"].initial = self.instance.directors.all()
            self.fields["tags"].initial = self.instance.tags.all()
            try:
                details = self.instance.details
            except FilmDetails.DoesNotExist:
                details = None
            if details:
                self.fields["budget"].initial = details.budget
                self.fields["box_office"].initial = details.box_office
                self.fields["duration"].initial = details.duration
                self.fields["filming_location"].initial = details.filming_location

    def _save_details(self, film):
        FilmDetails.objects.update_or_create(
            film=film,
            defaults={
                "budget": self.cleaned_data.get("budget"),
                "box_office": self.cleaned_data.get("box_office"),
                "duration": self.cleaned_data.get("duration"),
                "filming_location": self.cleaned_data.get("filming_location") or "",
            },
        )

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 255:
            raise ValidationError("Длина названия превышает 255 символов.")
        return title

    def clean_year(self):
        year = self.cleaned_data["year"]
        if year < 1888 or year > date.today().year:
            raise ValidationError(
                f"Год выпуска должен быть от 1888 до {date.today().year}."
            )
        return year

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        if not description:
            raise ValidationError("Описание обязательно для заполнения.")
        return description

    def clean_genres(self):
        genres = self.cleaned_data.get("genres")
        if not genres:
            raise ValidationError("Укажите хотя бы один жанр.")
        return genres

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        if not tags:
            raise ValidationError("Укажите хотя бы один тег.")
        return tags

    def clean_budget(self):
        budget = self.cleaned_data.get("budget")
        if budget is not None and budget < 0:
            raise ValidationError("Бюджет не может быть отрицательным.")
        return budget

    def clean_box_office(self):
        box_office = self.cleaned_data.get("box_office")
        if box_office is not None and box_office < 0:
            raise ValidationError("Сборы не могут быть отрицательными.")
        return box_office

    def save(self, commit=True):
        delete_replaced_or_cleared_file(
            self.instance, "poster", self.cleaned_data.get("poster")
        )
        instance = super().save(commit=False)
        if not instance.pk:
            instance.rating = 0.0
            instance.is_published = Films.Status.DRAFT
        if not instance.pk or "title" in self.changed_data:
            instance.slug = generate_unique_slug(instance.title, instance.pk)
        if commit:
            instance.save()
            instance.genres.set(self.cleaned_data.get("genres", []))
            instance.directors.set(self.cleaned_data.get("directors", []))
            instance.tags.set(self.cleaned_data.get("tags", []))
            self._save_details(instance)
        return instance


class FilmCommentForm(forms.Form):
    text = forms.CharField(
        label="Комментарий",
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "class": "film-comment-textarea",
                "rows": 3,
                "placeholder": "Напишите, что думаете о фильме…",
            }
        ),
    )

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise ValidationError("Комментарий не может быть пустым.")
        return text
