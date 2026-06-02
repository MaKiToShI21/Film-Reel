from django.conf import settings


def user_defaults(request):
    return {
        "default_user_image": settings.DEFAULT_USER_IMAGE,
    }
