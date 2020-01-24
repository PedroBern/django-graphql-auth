from functools import wraps

from .constants import Messages
from .exceptions import WrongUsage


def login_required(fn):
    @wraps(fn)
    def wrapper(cls, root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return cls(success=False, errors=Messages.UNAUTHENTICATED)
        return fn(cls, root, info, **kwargs)

    return wrapper


def verification_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(cls, root, info, **kwargs):
        user = info.context.user
        if not user.status.verified:
            return cls(success=False, errors=Messages.NOT_VERIFIED)
        return fn(cls, root, info, **kwargs)

    return wrapper


def secondary_email_required(fn):
    @wraps(fn)
    @verification_required
    def wrapper(cls, root, info, **kwargs):
        user = info.context.user
        if not user.status.secondary_email:
            return cls(success=False, errors=Messages.SECONDARY_EMAIL_REQUIRED)
        return fn(cls, root, info, **kwargs)

    return wrapper


def password_confirmation_required(fn):
    @wraps(fn)
    def wrapper(cls, root, info, **kwargs):
        try:
            field_name = next(
                i for i in kwargs.keys() if i in ["password", "old_password"]
            )
            password = kwargs[field_name]
        except Exception:
            raise WrongUsage(
                """
                @password_confirmation is supposed to be used on
                mutations with 'password' or 'old_password' field required.
                """
            )
        user = info.context.user
        if user.check_password(password):
            return fn(cls, root, info, **kwargs)
        errors = {field_name: Messages.INVALID_PASSWORD}
        return cls(success=False, errors=errors)

    return wrapper
