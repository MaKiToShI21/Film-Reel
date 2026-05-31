from django.contrib import admin, messages
from django.db.models import Count
from django.utils.safestring import mark_safe

from .models import Director, FilmComment, FilmCommentReaction, FilmDetails, Films, Genre, TagPost
from .permissions import can_manage_all_films, can_manage_catalog_metadata


admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Администрирование FilmReel"
admin.site.index_title = "Панель управления"


class SuperuserOnlyAdminMixin:
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ModeratorCatalogAdminMixin:
    def has_module_permission(self, request):
        return can_manage_all_films(request.user)

    def has_view_permission(self, request, obj=None):
        return can_manage_all_films(request.user)

    def has_add_permission(self, request):
        return can_manage_all_films(request.user)

    def has_change_permission(self, request, obj=None):
        return can_manage_all_films(request.user)

    def has_delete_permission(self, request, obj=None):
        return can_manage_all_films(request.user)


class MetadataAdminMixin:
    def has_module_permission(self, request):
        return can_manage_catalog_metadata(request.user)

    def has_view_permission(self, request, obj=None):
        return can_manage_catalog_metadata(request.user)

    def has_add_permission(self, request):
        return can_manage_catalog_metadata(request.user)

    def has_change_permission(self, request, obj=None):
        return can_manage_catalog_metadata(request.user)

    def has_delete_permission(self, request, obj=None):
        return can_manage_catalog_metadata(request.user)


class DirectorStatusFilter(admin.SimpleListFilter):
    title = "Статус режиссера"
    parameter_name = "director_status"

    def lookups(self, request, model_admin):
        return [
            ("has_director", "С режиссером"),
            ("no_director", "Без режиссера"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "has_director":
            return queryset.annotate(_directors_count=Count("directors")).filter(
                _directors_count__gt=0
            )
        if self.value() == "no_director":
            return queryset.annotate(_directors_count=Count("directors")).filter(
                _directors_count=0
            )
        return queryset


@admin.register(Films)
class FilmsAdmin(ModeratorCatalogAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "post_photo",
        "time_create",
        "is_published",
        "brief_info",
        "release_period",
    )
    list_display_links = ("title",)
    list_editable = ("is_published",)
    ordering = ["-time_create", "title"]
    list_per_page = 5
    search_fields = ["title"]
    list_filter = [DirectorStatusFilter, "is_published"]
    actions = ["set_published", "set_draft"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("genres", "directors", "tags")
    readonly_fields = ("post_photo", "time_create", "time_update")
    fields = [
        "title",
        "slug",
        "year",
        "rating",
        "description",
        "poster",
        "post_photo",
        "author",
        "genres",
        "directors",
        "tags",
        "is_published",
        "time_create",
        "time_update",
    ]

    @admin.display(description="Изображение")
    def post_photo(self, film: Films):
        if film.poster:
            return mark_safe(f"<img src='{film.poster.url}' width='50'>")
        return "Без фото"

    @admin.display(description="Краткое описание")
    def brief_info(self, film: Films):
        if not film.description:
            return "-"
        return film.description[:50] + ("..." if len(film.description) > 50 else "")

    @admin.display(description="Период")
    def release_period(self, film: Films):
        if film.year < 2000:
            return "Классика"
        if film.year < 2020:
            return "Современное"
        return "Новое"

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False

        query_fold = search_term.strip().casefold()
        matching_pks = [
            pk
            for pk, title in queryset.values_list("pk", "title")
            if title and query_fold in title.casefold()
        ]
        return queryset.filter(pk__in=matching_pks), False

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Films.Status.PUBLISHED)
        self.message_user(
            request,
            f"Изменено {count} записи(ей).",
            level=messages.SUCCESS,
        )

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Films.Status.DRAFT)
        self.message_user(
            request,
            f"{count} записи(ей) сняты с публикации!",
            level=messages.WARNING,
        )


@admin.register(Genre)
class GenreAdmin(MetadataAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TagPost)
class TagPostAdmin(MetadataAdminMixin, admin.ModelAdmin):
    list_display = ("id", "tag", "slug")
    search_fields = ("tag",)
    prepopulated_fields = {"slug": ("tag",)}


@admin.register(Director)
class DirectorAdmin(MetadataAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "age", "oscars_count", "m_count")
    search_fields = ("name", "bio")
    list_filter = ("oscars_count",)
    list_editable = ("oscars_count", "m_count")


@admin.register(FilmDetails)
class FilmDetailsAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "film",
        "duration",
        "budget",
        "box_office",
        "filming_location",
    )
    search_fields = ("film__title", "filming_location")
    list_filter = ("duration", "filming_location")


@admin.register(FilmComment)
class FilmCommentAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "film", "author", "time_create", "parent")
    search_fields = ("author__username", "text", "film__title")
    list_filter = ("time_create",)
    raw_id_fields = ("film", "parent", "author")


@admin.register(FilmCommentReaction)
class FilmCommentReactionAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "comment", "reactor_key", "value")
    list_filter = ("value",)
    raw_id_fields = ("comment",)
