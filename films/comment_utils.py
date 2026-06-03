from django.db.models import Count, Q

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


def _set_replies_prefetch_cache(comment, replies_by_parent):
    replies = replies_by_parent.get(comment.pk, [])
    comment._prefetched_objects_cache = getattr(comment, "_prefetched_objects_cache", {})
    comment._prefetched_objects_cache["replies"] = replies
    for reply in replies:
        _set_replies_prefetch_cache(reply, replies_by_parent)


def _iter_comment_tree(comments):
    for comment in comments:
        yield comment
        yield from _iter_comment_tree(comment.replies.all())


def get_film_comments(film):
    all_comments = list(
        _comment_queryset()
        .filter(film=film)
        .order_by("time_create")
    )

    replies_by_parent = {}
    root_comments = []
    for comment in all_comments:
        if comment.parent_id is None:
            root_comments.append(comment)
        else:
            replies_by_parent.setdefault(comment.parent_id, []).append(comment)

    for comment in all_comments:
        _set_replies_prefetch_cache(comment, replies_by_parent)

    return root_comments


def get_user_comment_reactions(request, comments):
    comment_ids = [comment.pk for comment in _iter_comment_tree(comments)]

    if not comment_ids:
        for comment in _iter_comment_tree(comments):
            comment.user_reaction = None
        return {}

    reactor_key = get_rater_key(request)
    reactions = {
        reaction.comment_id: reaction.value
        for reaction in FilmCommentReaction.objects.filter(
            comment_id__in=comment_ids,
            reactor_key=reactor_key,
        )
    }

    for comment in _iter_comment_tree(comments):
        comment.user_reaction = reactions.get(comment.pk)

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
