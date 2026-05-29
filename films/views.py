from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import AddFilmForm, AddFilmModelForm, UploadFileForm
from .models import Category, Films, TagPost, UploadFiles
from .utils import DataMixin


def _apply_search(queryset, search_query):
    if not search_query:
        return queryset
    q = search_query.strip()
    if not q:
        return queryset
    return queryset.filter(
        Q(title__icontains=q)
        | Q(description__icontains=q)
        | Q(genre__icontains=q)
    )


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


def _published_films_qs():
    return Films.published.select_related("cat", "director", "author").prefetch_related("tags")


class FilmsHome(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = _published_films_qs()
        return _apply_search(qs, self.request.GET.get("q", ""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title="Все опубликованные фильмы",
            cat_selected=0,
            search_query=search_query,
        )


class FilmsByGenre(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = _published_films_qs()
        name = self.kwargs["name"]
        if name != "all":
            qs = qs.filter(genre__iexact=name)
        return _apply_search(qs, self.request.GET.get("q", ""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs["name"]
        search_query = self.request.GET.get("q", "").strip()
        if name == "all":
            title = "Все опубликованные фильмы"
        else:
            title = f"Фильмы жанра: {name}"
        return self.get_mixin_context(
            context,
            title=title,
            cat_selected=0,
            search_query=search_query,
        )


class FilmsByYear(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = (
            Films.published.filter(year=self.kwargs["film_year"])
            .select_related("cat", "director")
            .prefetch_related("tags")
        )
        return _apply_search(qs, self.request.GET.get("q", ""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["film_year"]
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Фильмы {year} года",
            cat_selected=0,
            search_query=search_query,
        )


class FilmsByRating(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = (
            Films.published.filter(rating__gte=self.kwargs["film_rating"])
            .select_related("cat", "director")
            .prefetch_related("tags")
        )
        return _apply_search(qs, self.request.GET.get("q", ""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        rating = self.kwargs["film_rating"]
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Фильмы с рейтингом от {rating}",
            cat_selected=0,
            search_query=search_query,
        )


class FilmsCategory(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])

    def get_queryset(self):
        qs = (
            Films.published.filter(cat_id=self.category.pk)
            .select_related("cat", "director")
            .prefetch_related("tags")
        )
        return _apply_search(qs, self.request.GET.get("q", ""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Категория: {self.category.name}",
            cat_selected=self.category.pk,
            search_query=search_query,
        )


class FilmsTagList(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.tag = get_object_or_404(TagPost, slug=self.kwargs["tag_slug"])

    def get_queryset(self):
        qs = self.tag.films.filter(is_published=Films.Status.PUBLISHED).select_related(
            "cat",
            "director",
        ).prefetch_related("tags")
        return _apply_search(qs, self.request.GET.get("q", ""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Тег: {self.tag.tag}",
            cat_selected=None,
            search_query=search_query,
        )


class FilmDetail(DataMixin, DetailView):
    model = Films
    template_name = "films/film_detail.html"
    context_object_name = "film"
    slug_url_kwarg = "film_slug"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Films.published.select_related("cat", "director").prefetch_related("tags"),
            slug=self.kwargs[self.slug_url_kwarg],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["film"].title)


class AddFilmFormPage(DataMixin, FormView):
    form_class = AddFilmForm
    template_name = "films/add_film_form.html"
    title_page = "Добавление фильма: обычная форма"

    def form_valid(self, form):
        if Films.objects.filter(slug=form.cleaned_data["slug"]).exists():
            form.add_error("slug", "Фильм с таким URL уже существует.")
            return self.form_invalid(form)
        film = _create_film_from_form(form)
        if film.is_published == Films.Status.PUBLISHED:
            return redirect(film.get_absolute_url())
        return redirect("films:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class AddFilmModelPage(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddFilmModelForm
    template_name = "films/add_film_model.html"
    title_page = "Добавление фильма: форма модели"
    permission_required = "films.add_films"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        film = self.object
        if film.is_published == Films.Status.PUBLISHED:
            return film.get_absolute_url()
        return reverse_lazy("films:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class UploadFilePage(PermissionRequiredMixin, DataMixin, View):
    title_page = "Загрузка файла"
    permission_required = "films.view_films"
    raise_exception = True

    def get(self, request):
        form = UploadFileForm()
        context = self.get_mixin_context({"form": form, "uploaded_file": None})
        return render(request, "films/upload_file.html", context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_file = None
        if form.is_valid():
            uploaded_file = UploadFiles.objects.create(file=form.cleaned_data["file"])
        context = self.get_mixin_context({"form": form, "uploaded_file": uploaded_file})
        return render(request, "films/upload_file.html", context)


class AboutCatalog(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = "films/about.html"
    title_page = "О каталоге FilmReel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class FilmUpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Films
    fields = [
        "title",
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
    template_name = "films/add_film_model.html"
    title_page = "Редактирование фильма"
    permission_required = "films.change_films"

    def get_success_url(self):
        film = self.object
        if film.is_published == Films.Status.PUBLISHED:
            return film.get_absolute_url()
        return reverse_lazy("films:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class FilmDeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Films
    template_name = "films/film_confirm_delete.html"
    context_object_name = "film"
    success_url = reverse_lazy("films:home")
    title_page = "Удаление фильма"
    permission_required = "films.delete_films"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


def page_not_found(request, exception):
    return HttpResponseNotFound(
        "<h1>Ошибка 404: Страница не найдена</h1>"
        "<p>Проверьте правильность введенного адреса.</p>"
    )
