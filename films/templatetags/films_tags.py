from django import template

from films.permissions import can_change_film, can_delete_comment, can_delete_film

register = template.Library()


@register.filter
def user_can_change_film(film, user):
    return can_change_film(user, film)


@register.filter
def user_can_delete_film(film, user):
    return can_delete_film(user, film)


@register.filter
def user_can_delete_comment(comment, user):
    return can_delete_comment(user, comment)
