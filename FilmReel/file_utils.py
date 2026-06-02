def delete_replaced_or_cleared_file(instance, field_name, cleaned_value):
    if cleaned_value is None or not instance.pk:
        return

    stored_name = (
        instance.__class__._default_manager.filter(pk=instance.pk).values_list(
            field_name, flat=True
        ).first()
    )
    if not stored_name:
        return

    field = instance._meta.get_field(field_name)
    field.storage.delete(stored_name)
