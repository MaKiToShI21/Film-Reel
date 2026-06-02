from .utils import build_filters_query, get_selected_filters


def catalog_filters(request):
    selected = get_selected_filters(request)
    search_query = request.GET.get("q", "").strip()
    return {
        "selected_genres": selected["genres"],
        "selected_directors": selected["directors"],
        "selected_tags": selected["tags"],
        "filters_query": build_filters_query(request),
        "search_query": search_query,
        "has_active_filters": any(selected.values()),
    }
