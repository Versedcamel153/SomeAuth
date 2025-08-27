from django import template
from someauth.conf import get_quickauth_setting

register = template.Library()


@register.inclusion_tag("account/social_buttons.html")
def quickauth_social_buttons():
    """
    Renders social login buttons based on QUICKAUTH settings.
    Usage in templates:
        {% load quickauth_tags %}
        {% quickauth_social_buttons %}
    """
    return {
        "USE_SOCIAL": get_quickauth_setting("USE_SOCIAL"),
        "ENABLED_PROVIDERS": get_quickauth_setting("ENABLED_PROVIDERS"),
    }