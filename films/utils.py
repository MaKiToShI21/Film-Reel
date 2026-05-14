from django.db.models import Count

from .models import Category


def get_categories_with_films():
    return (
        Category.objects.annotate(total_films=Count("films")).filter(total_films__gt=0)
    )


class DataMixin:
    title_page = None
    paginate_by = 3

    def get_mixin_context(self, context, **kwargs):
        if self.title_page is not None:
            context["title"] = self.title_page
        context.setdefault("categories", get_categories_with_films())
        context.setdefault("cat_selected", None)
        context.setdefault("search_query", "")
        context.update(kwargs)
        return context
