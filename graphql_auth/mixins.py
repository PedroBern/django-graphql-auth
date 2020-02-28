from smtplib import SMTPException

from django.core.signing import BadSignature, SignatureExpired
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.db import transaction

import graphene

from graphql_jwt.exceptions import JSONWebTokenError, JSONWebTokenExpired
from graphql_jwt.decorators import token_auth

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
    InvalidCredentials,
)
from .constants import Messages, TokenAction
from .utils import revoke_user_refresh_token, get_token_paylod, using_refresh_tokens
from .shortcuts import get_user_by_email, get_user_to_login
from .decorators import (
    password_confirmation_required,
    verification_required,
    secondary_email_required,
)

UserModel = get_user_model()


class RegisterMixin(Output):
    """
    Register user with fields defined in the settings.

    If the email field of the user model is part of the
    registration fields (default), check if there is
    no user with that email or as a secondary email.

    If it exists, it does not register the user,
    even if the email field is not defined as unique
    (default of the default django user model).

    When creating the user, it also creates a `UserStatus`
    related to that user, making it possible to track
    if the user is archived, verified and has a secondary
    email.

    Send account verification email.

    If allowed to not verified users login, return token.
    """

    form = RegisterForm

    @classmethod
    def Field(cls, *args, **kwargs):
        if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
            if using_refresh_tokens():
                cls._meta.fields["refresh_token"] = graphene.Field(graphene.String)
            cls._meta.fields["token"] = graphene.Field(graphene.String)
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def login_on_register(cls, root, info, **kwargs):
        return cls()

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                f = cls.form(kwargs)
                if f.is_valid():
                    email = kwargs.get(UserModel.EMAIL_FIELD, False)
                    UserStatus.clean_email(email)
                    user = f.save()
                    send_activation = (
                        app_settings.SEND_ACTIVATION_EMAIL is True and email
                    )
                    if send_activation:
                        user.status.send_activation_email(info)
                    if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
                        payload = cls.login_on_register(
                            root, info, password=kwargs.get("password1"), **kwargs
                        )
                        return_value = {}
                        for field in cls._meta.fields:
                            return_value[field] = getattr(payload, field)
                        return cls(**return_value)
                    return cls(success=True)
                else:
                    return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(
                success=False,
                # if the email was set as a secondary email,
                # the RegisterForm will not catch it,
                # so we need to run UserStatus.clean_email(email)
                errors={UserModel.EMAIL_FIELD: Messages.EMAIL_IN_USE},
            )
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)


class VerifyAccountMixin(Output):
    """
    Verify user account.

    Receive the token that was sent by email.
    If the token is valid, make the user verified
    by making the `user.status.verified` field true.
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
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class VerifySecondaryEmailMixin(Output):
    """
    Verify user secondary email.

    Receive the token that was sent by email.
    User is already verified when using this mutation.

    If the token is valid, add the secondary email
    to `user.status.secondary_email` field.

    Note that until the secondary email is verified,
    it has not been saved anywhere beyond the token,
    so it can still be used to create a new account.
    After being verified, it will no longer be available.
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.get("token")
            UserStatus.verify_secondary_email(token)
            return cls(success=True)
        except EmailAlreadyInUse:
            # while the token was sent and the user haven't
            # verified, the email was free. If other account
            # was created with it, it is already in use.
            return cls(success=False, errors=Messages.EMAIL_IN_USE)
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class ResendActivationEmailMixin(Output):
    """
    Sends activation email.

    It is called resend because theoretically
    the first activation email was sent when
    the user registered.

    If there is no user with the requested email,
    a successful response is returned.
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
            return cls(success=False, errors={"email": Messages.ALREADY_VERIFIED})


class SendPasswordResetEmailMixin(Output):
    """
    Send password reset email.

    For non verified users, send an activation
    email instead.

    Accepts both primary and secondary email.

    If there is no user with the requested email,
    a successful response is returned.
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
                    success=False,
                    errors={"email": Messages.NOT_VERIFIED_PASSWORD_RESET},
                )
            except SMTPException:
                return cls(success=False, errors=Messages.EMAIL_FAIL)


class PasswordResetMixin(Output):
    """
    Change user password without old password.

    Receive the token that was sent by email.

    If token and new passwords are valid, update
    user password and in case of using refresh
    tokens, revoke all of them.
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
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class ObtainJSONWebTokenMixin(Output):
    """
    Obtain JSON web token for given user.

    Allow to perform login with different fields,
    and secondary email if set. The fields are
    defined on settings.

    Not verified users can login by default. This
    can be changes on settings.

    If user is archived, make it unarchive and
    return `unarchiving=True` on output.
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
                password = kwargs.get("password")
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
            if user.status.archived is True:  # unarchive on login
                UserStatus.unarchive(user)
                unarchiving = True

            if user.status.verified or app_settings.ALLOW_LOGIN_NOT_VERIFIED:
                return cls.parent_resolve(
                    root, info, unarchiving=unarchiving, **next_kwargs
                )
            if user.check_password(password):
                raise UserNotVerified
            raise InvalidCredentials
        except (JSONWebTokenError, ObjectDoesNotExist, InvalidCredentials):
            return cls(success=False, errors=Messages.INVALID_CREDENTIALS)
        except UserNotVerified:
            return cls(success=False, errors=Messages.NOT_VERIFIED)


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
    Archive account and revoke refresh tokens.

    User must be verified and confirm password.
    """

    @classmethod
    def resolve_action(cls, user, *args, **kwargs):
        UserStatus.archive(user)
        revoke_user_refresh_token(user=user)


class DeleteAccountMixin(ArchiveOrDeleteMixin):
    """
    Delete account permanently or make `user.is_active=False`.

    The behavior is defined on settings.
    Anyway user refresh tokens are revoked.

    User must be verified and confirm password.
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
    Change account password when user knows the old password.

    A new token and refresh token are sent. User must be verified.
    """

    form = PasswordChangeForm

    @classmethod
    def Field(cls, *args, **kwargs):
        if using_refresh_tokens():
            cls._meta.fields["refresh_token"] = graphene.Field(graphene.String)
        cls._meta.fields["token"] = graphene.Field(graphene.String)
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def login_on_password_change(cls, root, info, **kwargs):
        return cls()

    @classmethod
    @verification_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        f = cls.form(user, kwargs)
        if f.is_valid():
            revoke_user_refresh_token(user)
            user = f.save()
            payload = cls.login_on_password_change(
                root,
                info,
                password=kwargs.get("new_password1"),
                **{user.USERNAME_FIELD: getattr(user, user.USERNAME_FIELD)}
            )
            return_value = {}
            for field in cls._meta.fields:
                return_value[field] = getattr(payload, field)
            return cls(**return_value)
        else:
            return cls(success=False, errors=f.errors.get_json_data())


class UpdateAccountMixin(Output):
    """
    Update user model fields, defined on settings.

    User must be verified.
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
    """
    Same as `grapgql_jwt` implementation, with standard output.
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            return cls.parent_resolve(root, info, **kwargs)
        except JSONWebTokenExpired:
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except JSONWebTokenError:
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class SendSecondaryEmailActivationMixin(Output):
    """
    Send activation to secondary email.

    User must be verified and confirm password.
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
            # while the token was sent and the user haven't verified,
            # the email was free. If other account was created with it
            # it is already in use
            return cls(success=False, errors={"email": Messages.EMAIL_IN_USE})
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)


class SwapEmailsMixin(Output):
    """
    Swap between primary and secondary emails.

    Require password confirmation.
    """

    @classmethod
    @secondary_email_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, **kwargs):
        info.context.user.status.swap_emails()
        return cls(success=True)


class RemoveSecondaryEmailMixin(Output):
    """
    Remove user secondary email.

    Require password confirmation.
    """

    @classmethod
    @secondary_email_required
    @password_confirmation_required
    def resolve_mutation(cls, root, info, **kwargs):
        info.context.user.status.remove_secondary_email()
        return cls(success=True)
