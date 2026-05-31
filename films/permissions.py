MODERATOR_GROUP_NAME = "Модератор"


def is_moderator(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=MODERATOR_GROUP_NAME).exists()


def can_manage_all_films(user):
    return user.is_authenticated and (user.is_superuser or is_moderator(user))


def can_change_film(user, film):
    if not user.is_authenticated:
        return False
    if user.is_superuser or is_moderator(user):
        return True
    return film.author_id == user.pk


def can_delete_film(user, film):
    return can_change_film(user, film)


def can_manage_catalog_metadata(user):
    return user.is_authenticated and (user.is_superuser or is_moderator(user))
