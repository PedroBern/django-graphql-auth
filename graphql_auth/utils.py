import re
from collections import Mapping

from django.core import signing
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def get_token(user, action, exp=None):
    username = user.get_username()
    if hasattr(username, "pk"):
        username = username.pk
    payload = {user.USERNAME_FIELD: username, "action": action}
    token = signing.dumps(payload)
    return token


def get_token_paylod(token, action, exp=None):
    payload = signing.loads(token, max_age=exp)
    _action = payload.pop("action")
    if _action != action:
        raise Exception("Invalid token.")
    return payload


def is_archived_user(user):
    if not user.is_active and user.last_login:
        return True
    return False


def is_not_verified_user(user):
    if not user.is_active and not user.last_login:
        return True
    return False


def get_token_field_name(dt, default=None):
    """
    return the token field name, can be
    'token', 'refresh_token',
    """
    return next(
        (i for i in dt.keys() if i in ["token", "refresh_token"]), default,
    )
