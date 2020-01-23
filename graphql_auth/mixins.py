from smtplib import SMTPException

from django.core.signing import BadSignature, SignatureExpired
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.db import transaction

from graphql_jwt.exceptions import JSONWebTokenError, JSONWebTokenExpired

from .forms import RegisterForm, EmailForm, UpdateAccountForm
from .bases import Output
from .models import UserStatus
from .settings import graphql_auth_settings as app_settings
from .exceptions import (
    UserAlreadyVerified,
    UserNotVerified,
    WrongUsage,
    TokenScopeError,
    EmailAlreadyInUse,
)
from .constants import Messages, TokenAction
from .utils import (
    revoke_user_refresh_token,
    get_token_paylod,
    get_token_field_name,
)
from .shortcuts import get_user_by_email, get_user_to_login
from .decorators import (
    password_confirmation_required,
    verification_required,
    secondary_email_required,
)

UserModel = get_user_model()


class RegisterMixin(Output):
    """
    register user with fields defined in settings
    """

    form = RegisterForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                f = cls.form(kwargs)
                if f.is_valid():
                    email = kwargs.get("email", False)
                    UserStatus.clean_email(email)
                    user = f.save()
                    user_status = UserStatus(user=user)
                    user_status.save()
                    send_activation = (
                        app_settings.SEND_ACTIVATION_EMAIL == True and email
                    )
                    if send_activation:
                        user_status.send_activation_email(info)
                    return cls(success=True)
                else:
                    return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(success=False, errors={"email": Messages.EMAIL_IN_USE})
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)


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
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRATED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class VerifySecondaryEmailMixin(Output):
    """
    verify secondary email. User is already verified.
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.get("token")
            UserStatus.verify_secondary_email(token)
            return cls(success=True)
        except EmailAlreadyInUse:
            return cls(success=False, errors=Messages.EMAIL_IN_USE)
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRATED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


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
            return cls(
                success=False, errors={"email": Messages.ALREADY_VERIFIED}
            )


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
                user.status.send_password_reset_email(info, [email])
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except ObjectDoesNotExist:
            return cls(success=True)  # even if user is not registred
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except UserNotVerified:
            user = get_user_by_email(email)
            try:
                user.status.resend_activation_email(info)
                return cls(
                    success=False, errors=Messages.NOT_VERIFIED_PASSWORD_RESET
                )
            except SMTPException:
                return cls(success=False, errors=Messages.EMAIL_FAIL)


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
                TokenAction.PASSWORD_RESET,
                app_settings.EXPIRATION_PASSWORD_RESET_TOKEN,
            )
            user = UserModel._default_manager.get(**payload)
            f = cls.form(user, kwargs)
            if f.is_valid():
                revoke_user_refresh_token(user)
                user = f.save()
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRATED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class ObtainJSONWebTokenMixin(Output):
    """
    Perform login.
    If user is archived, make it unarchived again.

    Allow login with different fields than USERNAME_FIELD
    deffined in settings.LOGIN_ALLOWED_FIELDS
    """

    @classmethod
    def resolve(cls, root, info, **kwargs):
        unarchiving = kwargs.get("unarchiving", False)
        return cls(user=info.context.user, unarchiving=unarchiving)

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        if len(kwargs.items()) != 2:
            raise WrongUsage(
                "Must login with password and one of the following fields %s."
                % (app_settings.LOGIN_ALLOWED_FIELDS)
            )

        try:
            next_kwargs = None
            USERNAME_FIELD = UserModel.USERNAME_FIELD
            unarchiving = False

            # extract USERNAME_FIELD to use in query
            if USERNAME_FIELD in kwargs:
                query_kwargs = {USERNAME_FIELD: kwargs[USERNAME_FIELD]}
                next_kwargs = kwargs
            else:  # use what is left to query
                password = kwargs.pop("password")
                query_field, query_value = kwargs.popitem()
                query_kwargs = {query_field: query_value}

            user = get_user_to_login(**query_kwargs)

            if not next_kwargs:
                next_kwargs = {
                    "password": password,
                    USERNAME_FIELD: getattr(user, USERNAME_FIELD),
                }
            if user.status.archived == True:  # unarchive on login
                UserStatus.unarchive(user)
                unarchiving = True
            return cls.parent_resolve(
                root, info, unarchiving=unarchiving, **next_kwargs
            )
        except (JSONWebTokenError, ObjectDoesNotExist):
            return cls(success=False, errors=Messages.INVALID_CREDENTIALS)


class ArchiveOrDeleteMixin(Output):
    @classmethod
    @verification_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, *args, **kwargs):
        user = info.context.user
        cls.resolve_action(user, root=root, info=info)
        return cls(success=True)


class ArchiveAccountMixin(ArchiveOrDeleteMixin):
    """
    Archive account and revoke refresh tokens
    """

    @classmethod
    def resolve_action(cls, user, *args, **kwargs):
        UserStatus.archive(user)
        revoke_user_refresh_token(user=user)


class DeleteAccountMixin(ArchiveOrDeleteMixin):
    """
    Delete account or turn is_active to False
    and revoke tokens. Based on settings
    """

    @classmethod
    def resolve_action(cls, user, *args, **kwargs):
        if app_settings.ALLOW_DELETE_ACCOUNT:
            revoke_user_refresh_token(user=user)
            user.delete()
        else:
            user.is_active = False
            user.save(update_fields=["is_active"])
            revoke_user_refresh_token(user=user)


class PasswordChangeMixin(Output):
    """
    Change account password when user remenbers the old password
    """

    form = PasswordChangeForm

    @classmethod
    @verification_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        f = cls.form(user, kwargs)
        if f.is_valid():
            revoke_user_refresh_token(user)
            user = f.save()
            return cls(success=True)
        else:
            return cls(success=False, errors=f.errors.get_json_data())


class UpdateAccountMixin(Output):
    """
    Update user models fields
    """

    form = UpdateAccountForm

    @classmethod
    @verification_required
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        f = cls.form(kwargs, instance=user)
        if f.is_valid():
            f.save()
            return cls(success=True)
        else:
            return cls(success=False, errors=f.errors.get_json_data())


class VerifyOrRefreshOrRevokeTokenMixin(Output):
    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            return cls.parent_resolve(root, info, **kwargs)
        except JSONWebTokenExpired:
            message = Messages.EXPIRATED_TOKEN
        except JSONWebTokenError:
            message = Messages.INVALID_TOKEN

        token_field_name = get_token_field_name(
            cls._meta.arguments
        ) or get_token_field_name(
            cls._meta.arguments["input"]._meta.fields, "token"
        )
        return cls(success=False, errors={token_field_name: message})


class SendSecondaryEmailActivationMixin(Output):
    """
    send activation to secondary email
    """

    @classmethod
    @verification_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email")
            f = EmailForm({"email": email})
            if f.is_valid():
                user = info.context.user
                user.status.send_secondary_email_activation(info, email)
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(success=False, errors=Messages.EMAIL_IN_USE)
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)


class SwapEmailsMixin(Output):
    """
    swap between primary and secondary emails
    """

    @classmethod
    @secondary_email_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, **kwargs):
        info.context.user.status.swap_emails()
        return cls(success=True)
