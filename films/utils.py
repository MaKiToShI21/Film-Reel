from django.db.models import Count, Q

from .models import Director, Films, Genre, TagPost

_PUBLISHED_FILTER = Q(films__is_published=Films.Status.PUBLISHED)

SORT_DATE = "date"
SORT_RATING = "rating"
SORT_DEFAULT = SORT_DATE

SORT_OPTIONS = {
    SORT_DATE: "-time_create",
    SORT_RATING: "-rating",
}


def get_directors_with_films():
    return (
        Director.objects.annotate(total_films=Count("films", filter=_PUBLISHED_FILTER))
        .filter(total_films__gt=0)
        .order_by("name")
    )


def get_tags_with_films():
    return (
        TagPost.objects.annotate(total_films=Count("films", filter=_PUBLISHED_FILTER))
        .filter(total_films__gt=0)
        .order_by("tag")
    )


def get_genres_with_films():
    return (
        Genre.objects.annotate(total_films=Count("films", filter=_PUBLISHED_FILTER))
        .filter(total_films__gt=0)
        .order_by("name")
    )


def _parse_int_list(values):
    result = []
    for value in values:
        if str(value).isdigit():
            result.append(int(value))
    return result


def get_selected_filters(request):
    return {
        "genres": _parse_int_list(request.GET.getlist("genre")),
        "directors": _parse_int_list(request.GET.getlist("director")),
        "tags": _parse_int_list(request.GET.getlist("tag")),
    }


def get_sort_by(request):
    sort = request.GET.get("sort", SORT_DEFAULT)
    if sort not in SORT_OPTIONS:
        return SORT_DEFAULT
    return sort


def apply_catalog_sort(queryset, request):
    return queryset.order_by(SORT_OPTIONS[get_sort_by(request)])


def build_filters_query(request, *, include_search=True, page=None):
    from urllib.parse import urlencode

    selected = get_selected_filters(request)
    params = []
    for genre_id in selected["genres"]:
        params.append(("genre", genre_id))
    for director_id in selected["directors"]:
        params.append(("director", director_id))
    for tag_id in selected["tags"]:
        params.append(("tag", tag_id))
    sort = get_sort_by(request)
    if sort != SORT_DEFAULT:
        params.append(("sort", sort))
    if include_search:
        search_query = request.GET.get("q", "").strip()
        if search_query:
            params.append(("q", search_query))
    if page is not None:
        params.append(("page", page))
    return urlencode(params)


def apply_catalog_filters(queryset, request):
    selected = get_selected_filters(request)

    if selected["genres"]:
        queryset = queryset.filter(genres__id__in=selected["genres"])

    if selected["directors"]:
        queryset = queryset.filter(directors__id__in=selected["directors"])

    for tag_id in selected["tags"]:
        queryset = queryset.filter(tags__id=tag_id)

    if selected["tags"] or selected["genres"] or selected["directors"]:
        queryset = queryset.distinct()

    return queryset


def get_catalog_sidebar_context(request, *, path_tag_id=None):
    selected = get_selected_filters(request)
    selected_tags = list(selected["tags"])
    if path_tag_id is not None and path_tag_id not in selected_tags:
        selected_tags.append(path_tag_id)
    has_active_filters = bool(
        selected["genres"] or selected["directors"] or selected_tags
    )
    return {
        "genres": get_genres_with_films(),
        "directors": get_directors_with_films(),
        "tags": get_tags_with_films(),
        "selected_genres": selected["genres"],
        "selected_directors": selected["directors"],
        "selected_tags": selected_tags,
        "sort_by": get_sort_by(request),
        "filters_query": build_filters_query(request),
        "has_active_filters": has_active_filters,
    }


class DataMixin:
    title_page = None
    paginate_by = 5

    def get_mixin_context(self, context, *, path_tag_id=None, **kwargs):
        if self.title_page is not None:
            context["title"] = self.title_page
        context.setdefault("search_query", self.request.GET.get("q", "").strip())
        context.update(get_catalog_sidebar_context(self.request, path_tag_id=path_tag_id))
        context.update(kwargs)
        return context
