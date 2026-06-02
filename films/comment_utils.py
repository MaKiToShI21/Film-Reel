from django.db.models import Count, Prefetch, Q

from .models import FilmComment, FilmCommentReaction, Films
from .rating_utils import get_rater_key


def film_comments_enabled(film):
    return film.is_published == Films.Status.PUBLISHED


def _comment_queryset():
    return FilmComment.objects.select_related("author").annotate(
        likes_count=Count("reactions", filter=Q(reactions__value=FilmCommentReaction.LIKE)),
        dislikes_count=Count(
            "reactions",
            filter=Q(reactions__value=FilmCommentReaction.DISLIKE),
        ),
    )


def get_film_comments(film):
    reply_qs = _comment_queryset().order_by("time_create")
    return (
        _comment_queryset()
        .filter(film=film, parent__isnull=True)
        .prefetch_related(Prefetch("replies", queryset=reply_qs))
        .order_by("time_create")
    )


def get_user_comment_reactions(request, comments):
    comment_ids = []
    for comment in comments:
        comment_ids.append(comment.pk)
        comment_ids.extend(reply.pk for reply in comment.replies.all())

    if not comment_ids:
        for comment in comments:
            comment.user_reaction = None
            for reply in comment.replies.all():
                reply.user_reaction = None
        return {}

    reactor_key = get_rater_key(request)
    reactions = {
        reaction.comment_id: reaction.value
        for reaction in FilmCommentReaction.objects.filter(
            comment_id__in=comment_ids,
            reactor_key=reactor_key,
        )
    }

    for comment in comments:
        comment.user_reaction = reactions.get(comment.pk)
        for reply in comment.replies.all():
            reply.user_reaction = reactions.get(reply.pk)

    return reactions


def get_comment_reaction_counts(comment):
    counts = FilmCommentReaction.objects.filter(comment=comment).aggregate(
        likes=Count("pk", filter=Q(value=FilmCommentReaction.LIKE)),
        dislikes=Count("pk", filter=Q(value=FilmCommentReaction.DISLIKE)),
    )
    return counts["likes"], counts["dislikes"]


def set_comment_reaction(comment, reactor_key, value):
    if value not in (FilmCommentReaction.LIKE, FilmCommentReaction.DISLIKE):
        raise ValueError("Invalid reaction value.")

    existing = FilmCommentReaction.objects.filter(
        comment=comment,
        reactor_key=reactor_key,
    ).first()

    if existing:
        if existing.value == value:
            existing.delete()
            return None
        existing.value = value
        existing.save(update_fields=["value"])
        return value

    FilmCommentReaction.objects.create(
        comment=comment,
        reactor_key=reactor_key,
        value=value,
    )
    return value
