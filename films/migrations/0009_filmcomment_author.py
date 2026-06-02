from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_comment_authors(apps, schema_editor):
    FilmComment = apps.get_model("films", "FilmComment")
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)

    for comment in FilmComment.objects.all():
        author_name = getattr(comment, "author_name", None)
        if not author_name:
            comment.delete()
            continue
        user = User.objects.filter(username=author_name).first()
        if user is None:
            comment.delete()
            continue
        comment.author_id = user.pk
        comment.save(update_fields=["author_id"])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("films", "0008_alter_filmdetails_box_office_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="filmcomment",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="film_comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="filmcomment",
            name="time_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Время обновления"),
        ),
        migrations.RunPython(migrate_comment_authors, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="filmcomment",
            name="author_name",
        ),
        migrations.AlterField(
            model_name="filmcomment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="film_comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
    ]
