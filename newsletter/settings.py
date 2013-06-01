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


def get_confirm_email_action():
    """ Return confirm email settings for specific actions. """
    confirm_email = getattr(
        django_settings, "NEWSLETTER_CONFIRM_EMAIL", True
    )

    return {
    'subscribe': getattr(
        django_settings,
        "NEWSLETTER_CONFIRM_EMAIL_SUBSCRIBE",
        confirm_email
    ),
    'unsubscribe': getattr(
        django_settings,
        "NEWSLETTER_CONFIRM_EMAIL_UNSUBSCRIBE",
        confirm_email
    ),
    'update': getattr(
        django_settings,
        "NEWSLETTER_CONFIRM_EMAIL_UPDATE",
        confirm_email
    ),
}

CONFIRM_EMAIL_ACTION = get_confirm_email_action()
