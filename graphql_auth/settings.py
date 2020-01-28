"""
Settings for graphql_auth are all namespaced in the GRAPHQL_AUTH setting.
For example your project's `settings.py` file might look like this:
GRAPHQL_AUTH = {
    "LOGIN_ALLOWED_FIELDS": ["email", "username"],
    "SEND_ACTIVATION_EMAIL": True,
}
This module provides the `graphql_auth_settings` object, that is used to access
Graphene settings, checking for user settings first, then falling
back to the defaults.
"""

from django.conf import settings as django_settings
from django.test.signals import setting_changed

from datetime import timedelta

# Copied shamelessly from Graphene / Django REST Framework

DEFAULTS = {
    # if allow to login without verification,
    # the register mutation will return a token
    "ALLOW_LOGIN_NOT_VERIFIED": True,
    # mutations fields options
    "LOGIN_ALLOWED_FIELDS": ["email", "username"],
    "ALLOW_LOGIN_WITH_SECONDARY_EMAIL": True,
    # required fields on register, plus password1 and password2,
    # can be a dict like UPDATE_MUTATION_FIELDS setting
    "REGISTER_MUTATION_FIELDS": ["email", "username"],
    "REGISTER_MUTATION_FIELDS_OPTIONAL": [],
    # optional fields on update account, can be list of fields
    "UPDATE_MUTATION_FIELDS": {"first_name": "String", "last_name": "String"},
    # tokens
    "EXPIRATION_ACTIVATION_TOKEN": timedelta(days=7),
    "EXPIRATION_PASSWORD_RESET_TOKEN": timedelta(hours=1),
    "EXPIRATION_SECONDARY_EMAIL_ACTIVATION_TOKEN": timedelta(hours=1),
    # email stuff
    "EMAIL_FROM": getattr(django_settings, "DEFAULT_FROM_EMAIL", "test@email.com"),
    "SEND_ACTIVATION_EMAIL": True,
    # client: example.com/activate/token
    "ACTIVATION_PATH_ON_EMAIL": "activate",
    "ACTIVATION_SECONDARY_EMAIL_PATH_ON_EMAIL": "activate",
    # client: example.com/password-reset/token
    "PASSWORD_RESET_PATH_ON_EMAIL": "password-reset",
    # email subjects templates
    "EMAIL_SUBJECT_ACTIVATION": "email/activation_subject.txt",
    "EMAIL_SUBJECT_ACTIVATION_RESEND": "email/activation_subject.txt",
    "EMAIL_SUBJECT_SECONDARY_EMAIL_ACTIVATION": "email/activation_subject.txt",
    "EMAIL_SUBJECT_PASSWORD_RESET": "email/password_reset_subject.txt",
    # email templates
    "EMAIL_TEMPLATE_ACTIVATION": "email/activation_email.html",
    "EMAIL_TEMPLATE_ACTIVATION_RESEND": "email/activation_email.html",
    "EMAIL_TEMPLATE_SECONDARY_EMAIL_ACTIVATION": "email/activation_email.html",
    "EMAIL_TEMPLATE_PASSWORD_RESET": "email/password_reset_email.html",
    # query stuff
    "USER_NODE_EXCLUDE_FIELDS": ["password", "is_superuser"],
    "USER_NODE_FILTER_FIELDS": {
        "email": ["exact"],
        "username": ["exact", "icontains", "istartswith"],
        "is_active": ["exact"],
        "status__archived": ["exact"],
        "status__verified": ["exact"],
        "status__secondary_email": ["exact"],
    },
    # turn is_active to False instead
    "ALLOW_DELETE_ACCOUNT": False,
}


class GraphQLAuthSettings(object):
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:
        from graphql_auth.settings import settings
        print(settings)
    """

    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(django_settings, "GRAPHQL_AUTH", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid graphql_auth setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


graphql_auth_settings = GraphQLAuthSettings(None, DEFAULTS)


def reload_graphql_auth_settings(*args, **kwargs):
    global graphql_auth_settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "GRAPHQL_AUTH":
        graphql_auth_settings = GraphQLAuthSettings(value, DEFAULTS)


setting_changed.connect(reload_graphql_auth_settings)
