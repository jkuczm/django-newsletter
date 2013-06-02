from django.test.signals import setting_changed

from .. import settings, views


def update_confirm_configuration(**kwargs):
    """
    If any of NEWSLETTER_CONFIRM_EMAIL... or NEWSLETTER_CONFIRM_FORM... setting
    changes update variables storing their processed values.
    """

    for feature in ('EMAIL', 'FORM'):

        if kwargs['setting'].startswith('NEWSLETTER_CONFIRM_%s' % feature):
            new_confirm_configuration = \
                settings.get_confirm_configuration(feature)

            # Setting values in each module that imports CONFIRM_%s_ACTION
            # variable is ugly, but it's a consequence of using
            # "from <module> import ..." and not "import <module>."
            for mod in (settings, views):
                setattr(
                    mod,
                    'CONFIRM_%s_ACTION' % feature,
                    new_confirm_configuration,
                )

setting_changed.connect(update_confirm_configuration)
