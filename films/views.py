from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import AddFilmModelForm, FilmCommentForm
from .models import FilmComment, Films, TagPost
from .comment_utils import (
    film_comments_enabled,
    get_comment_reaction_counts,
    get_film_comments,
    get_user_comment_reactions,
    set_comment_reaction,
)
from .permissions import can_change_film, can_delete_film, can_manage_all_films
from .rating_utils import (
    clear_user_film_rating,
    get_rater_key,
    get_user_film_rating,
    set_user_film_rating,
)
from .utils import DataMixin, apply_catalog_filters, apply_catalog_sort, get_catalog_sidebar_context


def _get_safe_next_url(request, fallback):
    next_url = request.GET.get("next") or request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback


def _get_film_detail_back_url(request):
    return _get_safe_next_url(request, reverse("films:index", args=["all"]))


def _text_matches(query_fold, value):
    return bool(value) and query_fold in value.casefold()


def _apply_search(queryset, search_query):
    if not search_query:
        return queryset
    q = search_query.strip()
    if not q:
        return queryset

    query_fold = q.casefold()

    text_pks = {
        pk
        for pk, title, description in queryset.values_list("pk", "title", "description")
        if _text_matches(query_fold, title) or _text_matches(query_fold, description)
    }

    genre_pks = {
        pk
        for pk, genre_name in queryset.filter(genres__isnull=False)
        .values_list("pk", "genres__name")
        .distinct()
        if _text_matches(query_fold, genre_name)
    }

    matching_pks = text_pks | genre_pks
    if not matching_pks:
        return queryset.none()

    return queryset.filter(pk__in=matching_pks)


def _prepare_catalog_qs(qs, request):
    qs = apply_catalog_filters(qs, request)
    qs = _apply_search(qs, request.GET.get("q", ""))
    return apply_catalog_sort(qs, request)


def _published_films_qs():
    return Films.published.select_related("author").prefetch_related(
        "genres",
        "directors",
        "tags",
    )


class FilmsHome(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        return _prepare_catalog_qs(_published_films_qs(), self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title="Все опубликованные фильмы",
            search_query=search_query,
        )


class FilmsByGenre(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = _published_films_qs()
        name = self.kwargs["name"]
        if name != "all":
            qs = qs.filter(genres__name__iexact=name)
        return _prepare_catalog_qs(qs, self.request)

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
            search_query=search_query,
        )


class FilmsByYear(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = Films.published.filter(year=self.kwargs["film_year"]).prefetch_related(
            "genres",
            "directors",
            "tags",
        )
        return _prepare_catalog_qs(qs, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["film_year"]
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Фильмы {year} года",
            search_query=search_query,
        )


class FilmsByRating(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = Films.published.filter(
            rating__gte=self.kwargs["film_rating"]
        ).prefetch_related(
            "genres",
            "directors",
            "tags",
        )
        return _prepare_catalog_qs(qs, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        rating = self.kwargs["film_rating"]
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Фильмы с рейтингом от {rating}",
            search_query=search_query,
        )


class FilmsTagList(DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.tag = get_object_or_404(TagPost, slug=self.kwargs["tag_slug"])

    def get_queryset(self):
        qs = self.tag.films.filter(is_published=Films.Status.PUBLISHED).prefetch_related(
            "genres",
            "directors",
            "tags",
        )
        return _prepare_catalog_qs(qs, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title=f"Тег: {self.tag.tag}",
            search_query=search_query,
            path_tag_id=self.tag.id,
        )


class FilmDetail(DataMixin, DetailView):
    model = Films
    template_name = "films/film_detail.html"
    context_object_name = "film"
    slug_url_kwarg = "film_slug"

    def get_queryset(self):
        qs = Films.objects.select_related("author").prefetch_related(
            "genres",
            "directors",
            "tags",
            "details",
        )
        user = self.request.user
        if not user.is_authenticated:
            return qs.filter(is_published=Films.Status.PUBLISHED)
        if can_manage_all_films(user):
            return qs
        return qs.filter(
            Q(is_published=Films.Status.PUBLISHED) | Q(author=user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = context["film"]
        context["user_rating"] = get_user_film_rating(self.request, film)
        if film_comments_enabled(film):
            root_comments = get_film_comments(film)
            context["root_comments"] = root_comments
            context["comment_user_reactions"] = get_user_comment_reactions(
                self.request,
                root_comments,
            )
            context["comment_form"] = FilmCommentForm()
        context["default_user_image"] = settings.DEFAULT_USER_IMAGE
        context["back_url"] = _get_film_detail_back_url(self.request)
        return self.get_mixin_context(context, title=film.title)


class AddFilmModelPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddFilmModelForm
    template_name = "films/film_form.html"
    title_page = "Добавление фильма"

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
        return self.get_mixin_context(
            context,
            is_editing=False,
            submit_label="Добавить фильм",
            cancel_url=reverse("films:home"),
            form_subtitle="Заполните данные о фильме для каталога FilmReel.",
        )


class AboutCatalog(DataMixin, TemplateView):
    template_name = "films/about.html"
    title_page = "О нас"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class MyFilms(LoginRequiredMixin, DataMixin, ListView):
    template_name = "films/index.html"
    context_object_name = "films"

    def get_queryset(self):
        qs = (
            Films.objects.filter(author=self.request.user)
            .select_related("author")
            .prefetch_related("genres", "directors", "tags", "details")
        )
        return _prepare_catalog_qs(qs, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        return self.get_mixin_context(
            context,
            title="Мои фильмы",
            search_query=search_query,
        )


class FilmUpdatePage(LoginRequiredMixin, DataMixin, UpdateView):
    model = Films
    form_class = AddFilmModelForm
    template_name = "films/film_form.html"
    title_page = "Редактирование фильма"
    slug_url_kwarg = "name"
    slug_field = "slug"

    def get_object(self, queryset=None):
        film = super().get_object(queryset=queryset)
        if not can_change_film(self.request.user, film):
            raise PermissionDenied
        return film

    def get_success_url(self):
        film = self.object
        if film.is_published == Films.Status.PUBLISHED:
            fallback = film.get_absolute_url()
        else:
            fallback = reverse_lazy("films:home")
        return _get_safe_next_url(self.request, fallback)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            is_editing=True,
            submit_label="Сохранить изменения",
            cancel_url=_get_safe_next_url(
                self.request,
                self.object.get_absolute_url(),
            ),
            form_subtitle=f"Изменение записи «{self.object.title}».",
        )


class FilmDeletePage(LoginRequiredMixin, DataMixin, DeleteView):
    model = Films
    template_name = "films/film_confirm_delete.html"
    context_object_name = "film"
    title_page = "Удаление фильма"
    slug_url_kwarg = "name"
    slug_field = "slug"

    def get_object(self, queryset=None):
        film = super().get_object(queryset=queryset)
        if not can_delete_film(self.request.user, film):
            raise PermissionDenied
        return film

    def get_success_url(self):
        fallback = reverse("films:home")
        next_url = _get_safe_next_url(self.request, fallback)
        film_url = self.object.get_absolute_url()
        next_path = next_url.split("#", 1)[0]
        if next_path.rstrip("/") == film_url.rstrip("/"):
            return fallback
        return next_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = _get_safe_next_url(
            self.request,
            self.object.get_absolute_url(),
        )
        return self.get_mixin_context(context)


def _get_accessible_film(request, film_slug):
    qs = Films.objects.select_related("author", "details").prefetch_related(
        "genres",
        "directors",
        "tags",
    )
    user = request.user
    if not user.is_authenticated:
        qs = qs.filter(is_published=Films.Status.PUBLISHED)
    elif not can_manage_all_films(user):
        qs = qs.filter(
            Q(is_published=Films.Status.PUBLISHED) | Q(author=user)
        )
    return get_object_or_404(qs, slug=film_slug)


@require_POST
def rate_film(request, film_slug):
    film = _get_accessible_film(request, film_slug)
    rater_key = get_rater_key(request)
    if request.POST.get("action") == "cancel":
        rating = clear_user_film_rating(film, rater_key)
        return JsonResponse({"user_rating": None, "rating": rating})
    try:
        score = int(request.POST.get("score", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Некорректная оценка."}, status=400)
    if not 1 <= score <= 10:
        return JsonResponse({"error": "Оценка должна быть от 1 до 10."}, status=400)
    rating = set_user_film_rating(film, rater_key, score)
    return JsonResponse({"rating": rating, "user_rating": score})


@login_required
@require_POST
def post_film_comment(request, film_slug):
    film = _get_accessible_film(request, film_slug)
    if not film_comments_enabled(film):
        raise PermissionDenied
    form = FilmCommentForm(request.POST)
    if form.is_valid():
        parent = None
        parent_id = request.POST.get("parent_id")
        if parent_id:
            parent = get_object_or_404(FilmComment, pk=parent_id, film=film)
        FilmComment.objects.create(
            film=film,
            parent=parent,
            author=request.user,
            text=form.cleaned_data["text"],
        )
        return redirect(f"{film.get_absolute_url()}#comments")

    root_comments = get_film_comments(film)
    context = {
        "film": film,
        "user_rating": get_user_film_rating(request, film),
        "root_comments": root_comments,
        "comment_user_reactions": get_user_comment_reactions(request, root_comments),
        "comment_form": form,
        "title": film.title,
        "default_user_image": settings.DEFAULT_USER_IMAGE,
        "back_url": _get_film_detail_back_url(request),
    }
    context.update(get_catalog_sidebar_context(request))
    return render(request, "films/film_detail.html", context)


@login_required
@require_POST
def edit_film_comment(request, film_slug, comment_id):
    film = _get_accessible_film(request, film_slug)
    if not film_comments_enabled(film):
        raise PermissionDenied
    comment = get_object_or_404(
        FilmComment,
        pk=comment_id,
        film=film,
        author=request.user,
    )
    form = FilmCommentForm(request.POST)
    if form.is_valid():
        comment.text = form.cleaned_data["text"]
        comment.save(update_fields=["text", "time_update"])
    return redirect(f"{film.get_absolute_url()}#comment-{comment.pk}")


@login_required
@require_POST
def delete_film_comment(request, film_slug, comment_id):
    film = _get_accessible_film(request, film_slug)
    if not film_comments_enabled(film):
        raise PermissionDenied
    comment = get_object_or_404(
        FilmComment,
        pk=comment_id,
        film=film,
        author=request.user,
    )
    comment.delete()
    return redirect(f"{film.get_absolute_url()}#comments")


@require_POST
def vote_film_comment(request, film_slug, comment_id):
    film = _get_accessible_film(request, film_slug)
    if not film_comments_enabled(film):
        return JsonResponse({"error": "Комментарии недоступны."}, status=403)
    comment = get_object_or_404(FilmComment, pk=comment_id, film=film)
    try:
        value = int(request.POST.get("value", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Некорректная реакция."}, status=400)
    if value not in (1, -1):
        return JsonResponse({"error": "Некорректная реакция."}, status=400)

    user_reaction = set_comment_reaction(comment, get_rater_key(request), value)
    likes, dislikes = get_comment_reaction_counts(comment)
    return JsonResponse(
        {
            "user_reaction": user_reaction,
            "likes": likes,
            "dislikes": dislikes,
        }
    )


def page_not_found(request, exception):
    return HttpResponseNotFound(
        "<h1>Ошибка 404: Страница не найдена</h1>"
        "<p>Проверьте правильность введенного адреса.</p>"
    )
