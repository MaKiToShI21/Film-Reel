from django.db.models import Count, Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddFilmForm, AddFilmModelForm, UploadFileForm
from .models import Category, Films, TagPost, UploadFiles


def _get_categories_with_films():
    return Category.objects.annotate(total_films=Count("films")).filter(total_films__gt=0)


def _apply_search(queryset, search_query):
    if not search_query:
        return queryset

    return queryset.filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(genre__icontains=search_query)
    )


def _render_films_index(request, *, title, films, cat_selected=None):
    search_query = request.GET.get("q", "").strip()
    films = _apply_search(films, search_query)

    context = {
        "title": title,
        "films": films,
        "categories": _get_categories_with_films(),
        "cat_selected": cat_selected,
        "search_query": search_query,
    }
    return render(request, "films/index.html", context)


def home(request):
    films = Films.published.select_related("cat", "director").prefetch_related("tags")
    return _render_films_index(request, title="Все фильмы", films=films)


def index(request, name):
    if name == "all":
        films = Films.published.select_related("cat", "director").prefetch_related("tags")
        title = "Все фильмы"
    else:
        films = (
            Films.published.filter(genre__iexact=name)
            .select_related("cat", "director")
            .prefetch_related("tags")
        )
        title = f"Фильмы жанра: {name}"

    return _render_films_index(request, title=title, films=films)


def _create_film_from_form(form):
    film = Films.objects.create(
        title=form.cleaned_data["title"],
        slug=form.cleaned_data["slug"],
        year=form.cleaned_data["year"],
        rating=form.cleaned_data["rating"],
        genre=form.cleaned_data["genre"],
        description=form.cleaned_data["description"],
        is_published=form.cleaned_data["is_published"],
        cat=form.cleaned_data["cat"],
        director=form.cleaned_data["director"],
    )
    film.tags.set(form.cleaned_data["tags"])
    return film


def _redirect_after_save(film):
    if film.is_published == Films.Status.PUBLISHED:
        return redirect(film.get_absolute_url())
    return redirect("films:home")


def add_film_form(request):
    if request.method == "POST":
        form = AddFilmForm(request.POST)
        if form.is_valid():
            if Films.objects.filter(slug=form.cleaned_data["slug"]).exists():
                form.add_error("slug", "Фильм с таким URL уже существует.")
            else:
                film = _create_film_from_form(form)
                return _redirect_after_save(film)
    else:
        form = AddFilmForm()

    return render(
        request,
        "films/add_film_form.html",
        {"title": "Добавление фильма: обычная форма", "form": form},
    )


def add_film_model(request):
    if request.method == "POST":
        form = AddFilmModelForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            return _redirect_after_save(film)
    else:
        form = AddFilmModelForm()

    return render(
        request,
        "films/add_film_model.html",
        {"title": "Добавление фильма: форма модели", "form": form},
    )


def upload_file(request):
    uploaded_file = None

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadFiles.objects.create(file=form.cleaned_data["file"])
    else:
        form = UploadFileForm()

    return render(
        request,
        "films/upload_file.html",
        {
            "title": "Загрузка файла",
            "form": form,
            "uploaded_file": uploaded_file,
        },
    )


def film_detail(request, film_slug):
    film = get_object_or_404(
        Films.objects.select_related("cat", "director").prefetch_related("tags"),
        slug=film_slug,
        is_published=Films.Status.PUBLISHED,
    )

    context = {
        "title": film.title,
        "film": film,
    }
    return render(request, "films/film_detail.html", context)


def films_by_year(request, film_year):
    films = (
        Films.published.filter(year=film_year)
        .select_related("cat", "director")
        .prefetch_related("tags")
    )
    return _render_films_index(
        request,
        title=f"Фильмы {film_year} года",
        films=films,
    )


def films_by_rating(request, film_rating):
    films = (
        Films.published.filter(rating__gte=film_rating)
        .select_related("cat", "director")
        .prefetch_related("tags")
    )
    return _render_films_index(
        request,
        title=f"Фильмы с рейтингом от {film_rating}",
        films=films,
    )


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    films = (
        Films.published.filter(cat_id=category.pk)
        .select_related("cat", "director")
        .prefetch_related("tags")
    )

    return _render_films_index(
        request,
        title=f"Категория: {category.name}",
        films=films,
        cat_selected=category.pk,
    )


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    films = tag.films.filter(is_published=Films.Status.PUBLISHED).select_related(
        "cat", "director"
    )

    return _render_films_index(
        request,
        title=f"Тег: {tag.tag}",
        films=films,
    )


def page_not_found(request, exception):
    return HttpResponseNotFound(
        "<h1>Ошибка 404: Страница не найдена</h1>"
        "<p>Проверьте правильность введенного адреса.</p>"
    )
