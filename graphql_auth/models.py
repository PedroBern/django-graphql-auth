from django.db import models
from django.conf import settings as django_settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model


from .settings import graphql_auth_settings as app_settings
from .utils import get_token, get_token_paylod
from .exceptions import UserAlreadyVerified, UserNotVerified


class UserStatus(models.Model):
    """
    A helper model that handles user account stuff.
    """

    user = models.OneToOneField(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="status",
    )
    verified = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def send(self, subject, template, context):
        _subject = render_to_string(subject).replace("\n", " ").strip()
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        return send_mail(
            subject=_subject,
            from_email=app_settings.EMAIL_FROM,
            message=message,
            html_message=html_message,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def get_email_context(self, info, path, action, exp):
        token = get_token(self.user, action, exp)
        site = get_current_site(info.context)
        return {
            "user": self.user,
            "token": token,
            "port": info.context.get_port(),
            "site_name": site.name,
            "domain": site.domain,
            "protocol": "https" if info.context.is_secure() else "http",
            "path": path,
        }

    def send_activation_email(self, info):
        email_context = self.get_email_context(
            info,
            app_settings.ACTIVATION_PATH_ON_EMAIL,
            "activation",
            app_settings.EXPIRATION_ACTIVATION_TOKEN,
        )
        template = app_settings.EMAIL_TEMPLATE_ACTIVATION
        subject = app_settings.EMAIL_SUBJECT_ACTIVATION
        return self.send(subject, template, email_context)

    def resend_activation_email(self, info):
        if self.verified == True:
            raise UserAlreadyVerified
        email_context = self.get_email_context(
            info,
            app_settings.ACTIVATION_PATH_ON_EMAIL,
            "activation",
            app_settings.EXPIRATION_ACTIVATION_TOKEN,
        )
        template = app_settings.EMAIL_TEMPLATE_RESEND_ACTIVATION
        subject = app_settings.EMAIL_SUBJECT_RESEND_ACTIVATION
        return self.send(subject, template, email_context)

    def send_password_reset_email(self, info):
        if self.verified == False:
            raise UserNotVerified
        email_context = self.get_email_context(
            info,
            app_settings.PASSWORD_RESET_PATH_ON_EMAIL,
            "password_reset",
            app_settings.EXPIRATION_PASSWORD_RESET_TOKEN,
        )
        template = app_settings.EMAIL_TEMPLATE_PASSWORD_RESET
        subject = app_settings.EMAIL_SUBJECT_PASSWORD_RESET
        return self.send(subject, template, email_context)

    @classmethod
    def verify(cls, token):
        payload = get_token_paylod(
            token, "activation", app_settings.EXPIRATION_ACTIVATION_TOKEN,
        )
        user = get_user_model()._default_manager.get(**payload)
        user_status = cls.objects.get(user=user)
        if user_status.verified == False:
            user_status.verified = True
            user_status.save(update_fields=["verified"])
        else:
            raise UserAlreadyVerified

    @classmethod
    def unarchive(cls, user):
        user_status = cls.objects.get(user=user)
        if user_status.archived == True:
            user_status.archived = False
            user_status.save(update_fields=["archived"])

    @classmethod
    def archive(cls, user):
        user_status = cls.objects.get(user=user)
        if user_status.archived == False:
            user_status.archived = True
            user_status.save(update_fields=["archived"])
