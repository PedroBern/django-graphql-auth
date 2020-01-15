from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils.text import normalize_newlines

from .settings import settings


class EmailBase:
    from_email = settings.EMAIL_FROM

    @classmethod
    def get_message(cls, context):
        subject = render_to_string(cls.subject).replace("\n", " ").strip()
        html_message = render_to_string(cls.template, context)
        message = strip_tags(html_message)
        return subject, html_message, message

    @classmethod
    def send(cls, to, context={}):
        subject, html_message, message = cls.get_message(context)
        return send_mail(
            subject=subject,
            from_email=cls.from_email,
            message=message,
            html_message=html_message,
            recipient_list=[to],
            fail_silently=False,
        )


class ActivationEmail(EmailBase):
    template = settings.EMAIL_TEMPLATE_ACTIVATION
    subject = settings.EMAIL_SUBJECT_ACTIVATION


class ResendActivationEmail(EmailBase):
    template = settings.EMAIL_TEMPLATE_RESEND_ACTIVATION
    subject = settings.EMAIL_SUBJECT_RESEND_ACTIVATION


class PasswordResetEmail(EmailBase):
    template = settings.EMAIL_TEMPLATE_PASSWORD_RESET
    subject = settings.EMAIL_SUBJECT_PASSWORD_RESET
