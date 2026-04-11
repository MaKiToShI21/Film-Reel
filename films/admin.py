from django.contrib import admin, messages

from .models import Category, Director, FilmDetails, Films, TagPost


admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Администраторирование FilmReel"
admin.site.index_title = "Панель управления"


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
            return queryset.filter(director__isnull=False)
        if self.value() == "no_director":
            return queryset.filter(director__isnull=True)
        return queryset


@admin.register(Films)
class FilmsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "time_create",
        "is_published",
        "cat",
        "brief_info",
        "release_period",
    )
    list_display_links = ("title",)
    list_editable = ("is_published",)
    ordering = ["-time_create", "title"]
    list_per_page = 5
    search_fields = ["title__startswith", "cat__name"]
    list_filter = [DirectorStatusFilter, "cat__name", "is_published"]
    actions = ["set_published", "set_draft"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("time_create", "time_update")
    fields = [
        "title",
        "slug",
        "year",
        "rating",
        "genre",
        "description",
        "cat",
        "director",
        "tags",
        "poster",
        "is_published",
        "time_create",
        "time_update",
    ]

    @admin.display(description="Краткое описание")
    def brief_info(self, film: Films):
        if not film.description:
            return "—"
        return film.description[:50] + ("..." if len(film.description) > 50 else "")

    @admin.display(description="Период")
    def release_period(self, film: Films):
        if film.year < 2000:
            return "Классика"
        if film.year < 2020:
            return "Современное"
        return "Новое"

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ("id", "tag", "slug")
    search_fields = ("tag",)
    prepopulated_fields = {"slug": ("tag",)}


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "oscars_count", "m_count")
    search_fields = ("name", "bio")
    list_filter = ("oscars_count",)
    list_editable = ("oscars_count", "m_count")


@admin.register(FilmDetails)
class FilmDetailsAdmin(admin.ModelAdmin):
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
