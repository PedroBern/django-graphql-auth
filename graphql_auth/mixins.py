from smtplib import SMTPException

from django.core.signing import BadSignature
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

from graphql_jwt.exceptions import JSONWebTokenError

from .forms import RegisterForm, EmailForm
from .bases import Output
from .models import UserStatus
from .settings import graphql_auth_settings as app_settings
from .exceptions import UserAlreadyVerified, UserNotVerified
from .constants import Messages
from .utils import (
    get_user_by_email,
    revoke_user_refresh_token,
    get_token_paylod,
)


class RegisterMixin(Output):
    """
    register user with fields defined in settings
    """

    form = RegisterForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            f = cls.form(kwargs)
            if f.is_valid():
                user = f.save()
                user_status = UserStatus(user=user)
                user_status.save()
                send_activation = (
                    app_settings.SEND_ACTIVATION_EMAIL == True
                    and kwargs["email"]
                )
                if send_activation:
                    user_status.send_activation_email(info)
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except Exception as err:
            raise Exception(err)


class VerifyAccountMixin(Output):
    """
    verify user with token sent by email
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.get("token")
            UserStatus.verify(token)
            return cls(success=True)
        except UserAlreadyVerified:
            return cls(success=False, errors=Messages.ALREADY_VERIFIED)
        except BadSignature:
            return cls(success=False, errors=Messages.INVALID_TOKEN)
        except Exception as err:
            raise Exception(err)


class ResendActivationEmailMixin(Output):
    """
    resend an activation email
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email")
            f = EmailForm({"email": email})
            if f.is_valid():
                user = get_user_by_email(email)
                user.status.resend_activation_email(info)
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except ObjectDoesNotExist:
            return cls(success=True)  # even if user is not registred
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except UserAlreadyVerified:
            return cls(success=False, errors=Messages.ALREADY_VERIFIED)
        except Exception as err:
            raise Exception(err)


class SendPasswordResetEmailMixin(Output):
    """
    send password reset email
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email")
            f = EmailForm({"email": email})
            if f.is_valid():
                user = get_user_by_email(email)
                user.status.send_password_reset_email(info)
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except ObjectDoesNotExist:
            return cls(success=True)  # even if user is not registred
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except UserNotVerified:
            return cls(
                success=False, errors=Messages.NOT_VERIFIED_PASSWORD_RESET
            )
        except Exception as err:
            raise Exception(err)


class PasswordResetMixin(Output):
    """
    reset password
    """

    form = SetPasswordForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.pop("token")
            payload = get_token_paylod(
                token,
                "password_reset",
                app_settings.EXPIRATION_PASSWORD_RESET_TOKEN,
            )
            user = get_user_model()._default_manager.get(**payload)
            f = cls.form(user, kwargs)
            if f.is_valid():
                revoke_user_refresh_token(user)
                user = f.save()
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except BadSignature:
            return cls(success=False, errors=Messages.INVALID_TOKEN)
        except Exception as err:
            raise Exception(err)
