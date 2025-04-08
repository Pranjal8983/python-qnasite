from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def show_field_errors(field):
    """
    Returns an HTML representation of the error message for a
    field with custom styling
    """
    if field.errors:
        error_message = ""
        for error in field.errors:
            error_message = strip_tags(error)
        return mark_safe(
            f'<span id="validation-error" class="ajax-error form_errors\
                text-danger">{error_message}</span>'
        )
    return ""


@register.filter()
def show_non_field_errors(error):
    """
    Returns an HTML representation of the error message for a
    non-field with custom styling
    """
    if error:
        error_message = ""
        for error in error:
            error_message = strip_tags(error)
        return mark_safe(
            f'<span id="validation-error" class="ajax-error form_errors\
                text-danger">{error_message}</span>'
        )
    return ""


@register.filter()
def show_label(field):
    """
    Returns an HTML representation of the label with custom styling
    """
    required = ""
    if field.field.required:  # Check the field is required or not
        required = '<span class="text-danger">*</span>'
    else:
        required = ""

    return mark_safe(
        f'<label for="{field.label.lower().replace(" ", "_")}" \
            class="mb-3.6 text-sm text-dark-black-50">{field.label.title()} {required}</label>'
    )


@register.filter()
def convert_to_id(field):
    """
    Replaces the space in between the field names
    """
    return field.replace(" ", "_").lower()
