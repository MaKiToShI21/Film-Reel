from django.db import migrations

MODERATOR_GROUP_NAME = "Модератор"
OLD_MODERATOR_GROUP_NAME = "moderator"

MODERATOR_PERMISSIONS = (
    ("films", "films", ("add", "change", "delete", "view")),
    ("films", "genre", ("add", "change", "delete", "view")),
    ("films", "director", ("add", "change", "delete", "view")),
    ("films", "tagpost", ("add", "change", "delete", "view")),
)


def _collect_permissions(Permission, ContentType):
    permissions = []
    for app_label, model, actions in MODERATOR_PERMISSIONS:
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        for action in actions:
            permissions.append(
                Permission.objects.get(
                    content_type=content_type,
                    codename=f"{action}_{model}",
                )
            )
    return permissions


def sync_moderator_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    group, _ = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)
    required_permissions = _collect_permissions(Permission, ContentType)
    group.permissions.add(*required_permissions)

    Group.objects.filter(name=OLD_MODERATOR_GROUP_NAME).delete()


def revert_sync(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    group, _ = Group.objects.get_or_create(name=OLD_MODERATOR_GROUP_NAME)
    group.permissions.set(_collect_permissions(Permission, ContentType))


class Migration(migrations.Migration):
    dependencies = [
        ("films", "0010_moderator_group"),
    ]

    operations = [
        migrations.RunPython(sync_moderator_group, revert_sync),
    ]
