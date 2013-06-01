from django.test.signals import setting_changed

from .. import settings, views


def update_confirm_email(**kwargs):
    if kwargs['setting'] in (
            'NEWSLETTER_CONFIRM_EMAIL',
            'NEWSLETTER_CONFIRM_EMAIL_SUBSCRIBE',
            'NEWSLETTER_CONFIRM_EMAIL_UNSUBSCRIBE',
            'NEWSLETTER_CONFIRM_EMAIL_UPDATE',
    ):
        settings.CONFIRM_EMAIL_ACTION = settings.get_confirm_email_action()
        views.CONFIRM_EMAIL_ACTION = settings.CONFIRM_EMAIL_ACTION

setting_changed.connect(update_confirm_email)
