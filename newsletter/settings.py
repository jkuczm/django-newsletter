from django.conf import settings as django_settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from .utils import ACTIONS

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


def get_confirm_configuration(feature):
    """
    Return configuration of confirmation email or form
    for specific actions.
    """
    assert feature in ('EMAIL', 'FORM')

    global_setting_name = 'NEWSLETTER_CONFIRM_%s' % feature

    global_setting = getattr(
        django_settings, global_setting_name, True
    )

    configuration = {}

    for action in ACTIONS:
        configuration[action] = getattr(
            django_settings,
            "%s_%s" % (global_setting_name, action.upper()),
            global_setting
        )

    return configuration

CONFIRM_EMAIL_ACTION = get_confirm_configuration('EMAIL')

CONFIRM_FORM_ACTION = get_confirm_configuration('FORM')
