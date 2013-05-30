from django.conf import settings as django_settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured


# Import and set the richtext field
NEWSLETTER_RICHTEXT_WIDGET = \
    getattr(django_settings, "NEWSLETTER_RICHTEXT_WIDGET", "")

RICHTEXT_WIDGET = None
if NEWSLETTER_RICHTEXT_WIDGET:
    module, attr = NEWSLETTER_RICHTEXT_WIDGET.rsplit(".", 1)
    try:
        mod = import_module(module)
        RICHTEXT_WIDGET = getattr(mod, attr)
    except Exception as e:
        # Catch ImportError and other exceptions too
        # (e.g. user sets setting to an integer)
        raise ImproperlyConfigured(
            "Error while importing setting "
            "NEWSLETTER_RICHTEXT_WIDGET %r: %s" % (
                NEWSLETTER_RICHTEXT_WIDGET, e
            )
        )

# Global confirm email setting
# can be overridden by settings for specific actions
CONFIRM_EMAIL = getattr(
    django_settings, "NEWSLETTER_CONFIRM_EMAIL", True
)

# Process confirm email settings for specific actions
# if not set global setting is used.
CONFIRM_EMAIL_ACTION = {
    'subscribe': getattr(
        django_settings,
        "NEWSLETTER_CONFIRM_EMAIL_SUBSCRIBE",
        CONFIRM_EMAIL
    ),
    'unsubscribe': getattr(
        django_settings,
        "NEWSLETTER_CONFIRM_EMAIL_UNSUBSCRIBE",
        CONFIRM_EMAIL
    ),
    'update': getattr(
        django_settings,
        "NEWSLETTER_CONFIRM_EMAIL_UPDATE",
        CONFIRM_EMAIL
    ),
}
