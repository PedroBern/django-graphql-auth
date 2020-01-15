from .constants import Messages
from .utils import is_not_verified_user


def is_authenticated_and_verified(fn):
    """
    check if user is authenticated and verified
    return the class with args:
        success = False
        errors = ["Unauthenticated."]
    """

    def wrapper(cls, root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return cls(success=False, errors=Messages.UNAUTHENTICATED)
        elif is_not_verified_user(user):
            return cls(success=False, errors=Messages.NOT_VERIFIED)
        return fn(cls, root, info, **kwargs)

    return wrapper


def password_confirmation(fn,):
    """
    password required on inputs
    return the class with args:
        success = False
        errors = ...
    """

    def wrapper(cls, root, info, **kwargs):
        try:
            field_name = next(
                i for i in kwargs.keys() if i in ["password", "old_password"]
            )
            password = kwargs[field_name]
        except Exception:
            raise Exception(
                """
                @password_confirmation is supposed to be used on
                mutations with 'password' field required.
                """
            )
        user = info.context.user
        if user.check_password(password):
            return fn(cls, root, info, **kwargs)
        errors = {field_name: Messages.INVALID_PASSWORD}
        return cls(success=False, errors=errors)

    return wrapper
