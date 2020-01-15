"""
inspired by djoser.conf.py
https://github.com/sunscrapers/djoser/blob/master/djoser/conf.py
"""

from datetime import timedelta
from importlib import import_module

from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.functional import LazyObject


default_settings = {
    "LOGIN_ALLOWED_FIELDS": ["email", "username"],
    "MUTATION_FIELDS_REGISTER": ["email", "username"],
    "MUTATION_FIELDS_ARCHIVE": ["email"],
    "MUTATION_FIELDS_DELETE": ["email"],
    "MUTATION_FIELDS_UPDATE": {
        "username": "String",
        "first_name": "String",
        "last_name": "String",
    },
    "SEND_EMAIL_ACTIVATION": True,
    "EMAIL_URL_ACTIVATION": "activate",  # client: example.com/activate/token
    "EMAIL_URL_PASSWORD_RESET": "password-reset",  # client: example.com/password-reset/token
    "EXPIRATION_ACTIVATION_TOKEN": timedelta(days=7),
    "EXPIRATION_PASSWORD_RESET_TOKEN": timedelta(hours=1),
    "EMAIL_FROM": getattr(
        django_settings, "DEFAULT_FROM_EMAIL", "test@email.com"
    ),
    "EMAIL_SUBJECT_ACTIVATION": "email/activation_subject.txt",
    "EMAIL_SUBJECT_RESEND_ACTIVATION": "email/activation_subject.txt",
    "EMAIL_SUBJECT_PASSWORD_RESET": "email/password_reset_subject.txt",
    "EMAIL_TEMPLATE_ACTIVATION": "email/activation_email.html",
    "EMAIL_TEMPLATE_RESEND_ACTIVATION": "email/activation_email.html",
    "EMAIL_TEMPLATE_PASSWORD_RESET": "email/password_reset_email.html",
    "USER_NODE_EXCLUDE_FIELDS": ["password", "is_superuser"],
    "USER_NODE_FILTER_FIELDS": {
        "email": ["exact",],
        "username": ["exact", "icontains", "istartswith"],
    },
}


class Settings:
    def __init__(self, default_settings, explicit_overriden_settings=None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
            getattr(django_settings, "GRAP_AUTH", {})
            or explicit_overriden_settings
        )

        self._load_default_settings()
        self._override_settings(overriden_settings)

    def _load_default_settings(self):
        for setting_name, setting_value in default_settings.items():
            setattr(self, setting_name, setting_value)

    def _override_settings(self, overriden_settings):
        for setting_name, setting_value in overriden_settings.items():
            value = setting_value
            setattr(self, setting_name, value)


class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(default_settings, explicit_overriden_settings)


settings = LazySettings()


def reload_graph_auth_settings(*args, **kwargs):
    global settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "GRAP_AUTH":
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_graph_auth_settings)
