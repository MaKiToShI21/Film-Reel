from django.db import migrations

MODERATOR_GROUP_NAME = "moderator"

MODERATOR_PERMISSIONS = (
    ("films", "films", ("add", "change", "delete", "view")),
    ("films", "genre", ("add", "change", "delete", "view")),
    ("films", "director", ("add", "change", "delete", "view")),
    ("films", "tagpost", ("add", "change", "delete", "view")),
)


def create_moderator_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    group, _ = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)
    permissions = []
    for app_label, model, actions in MODERATOR_PERMISSIONS:
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        for action in actions:
            codename = f"{action}_{model}"
            permission = Permission.objects.get(
                content_type=content_type,
                codename=codename,
            )
            permissions.append(permission)
    group.permissions.set(permissions)


def remove_moderator_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=MODERATOR_GROUP_NAME).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("films", "0009_filmcomment_author"),
    ]

    operations = [
        migrations.RunPython(create_moderator_group, remove_moderator_group),
    ]
