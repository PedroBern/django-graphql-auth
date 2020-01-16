"""
    mixins
        [x] obtain json web token
        [x] verify_token
        [x] refresh_token
        [x] revoke_token
        [x] register
        [x] verify account
        [x] resend activation email
        [x] update user
        [x] archive account
        [x] delete account
        [x] password change
        [x] password reset email
        [x] password reset
        [ ] change primary email
        [ ] secondary email
"""

from datetime import datetime
from smtplib import SMTPException
import json

from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site


import graphene
from graphene import relay
import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenExpired, JSONWebTokenError
from graphql_jwt.decorators import login_required, permission_required

from .types import UserNode, ErrorType
from .utils import (
    get_token,
    get_token_paylod,
    is_archived_user,
    is_not_verified_user,
    get_token_field_name,
)
from .constants import Messages, TokenAction
from .settings import graphql_auth_settings as settings
from .email import ActivationEmail, ResendActivationEmail, PasswordResetEmail
from .decorators import is_authenticated_and_verified, password_confirmation
from .forms import (
    RegisterForm,
    UpdateAccountForm,
    EmailForm,
    PasswordChangeForm,
    SetPasswordForm,
)


class MutationMixin:
    """
    All mutations should extend this class
    """

    @classmethod
    def mutate(cls, root, info, **input):
        return cls.resolve_mutation(root, info, **input)

    @classmethod
    def parent_resolve(cls, root, info, **kwargs):
        return super().mutate(root, info, **kwargs)


class RelayMutationMixin:
    """
    All relay mutations should extend this class
    """

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return cls.resolve_mutation(root, info, **kwargs)

    @classmethod
    def parent_resolve(cls, root, info, **kwargs):
        return super().mutate_and_get_payload(root, info, **kwargs)


class Output:
    """
    All public classes should return success and errors
    """

    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(ErrorType)


class DynamicInputMixin:
    """
    get inputs from
        cls._inputs
        cls._required_inputs

    inputs is dict { input_name: input_type }
    or list [input_name,] -> defaults to String
    """

    _inputs = {}
    _required_inputs = {}

    @classmethod
    def Field(cls, *args, **kwargs):
        if isinstance(cls._inputs, dict):
            for key in cls._inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {
                        key: graphene.InputField(
                            getattr(graphene, cls._inputs[key])
                        )
                    }
                )
        elif isinstance(cls._inputs, list):
            for key in cls._inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {key: graphene.InputField(graphene.String)}
                )

        if isinstance(cls._required_inputs, dict):
            for key in cls._required_inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {
                        key: graphene.InputField(
                            getattr(graphene, cls._inputs[key], required=True)
                        )
                    }
                )
        elif isinstance(cls._required_inputs, list):
            for key in cls._required_inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {key: graphene.InputField(graphene.String, required=True)}
                )
        return super().Field(*args, **kwargs)


class DynamicArgsMixin:
    """
    get args from
        cls._args
        cls._required_args

    args is dict { arg_name: arg_type }
    or list [arg_name,] -> defaults to String
    """

    _args = {}
    _required_args = {}

    @classmethod
    def Field(cls, *args, **kwargs):
        if isinstance(cls._args, dict):
            for key in cls._args:
                cls._meta.arguments.update(
                    {key: graphene.Argument(getattr(graphene, cls._args[key]))}
                )
        elif isinstance(cls._args, list):
            for key in cls._args:
                cls._meta.arguments.update({key: graphene.String()})

        if isinstance(cls._required_args, dict):
            for key in cls._required_args:
                cls._meta.arguments.update(
                    {
                        key: graphene.Argument(
                            getattr(graphene, cls._args[key], required=True)
                        )
                    }
                )
        elif isinstance(cls._required_args, list):
            for key in cls._required_args:
                cls._meta.arguments.update(
                    {key: graphene.String(required=True)}
                )
        return super().Field(*args, **kwargs)


class ObtainJSONWebTokenMixin(Output):
    """
    Get token and allow access to user
    If user is archived, make it active
    Allow login with different fields, deffined in settings.LOGIN_ALLOWED_FIELDS
    """

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        """
        if not user.is_active and user.last_login: # and credentials ok
            # make user active
        """
        if len(kwargs.items()) != 2:
            raise Exception(
                "Must login with password and one of the following fields %s."
                % (settings.LOGIN_ALLOWED_FIELDS)
            )

        next_kwargs = None

        if get_user_model().USERNAME_FIELD in kwargs:
            query_kwargs = {
                get_user_model().USERNAME_FIELD: kwargs[
                    get_user_model().USERNAME_FIELD
                ]
            }
            next_kwargs = kwargs
        else:
            password = kwargs.pop("password")
            query_field, query_value = kwargs.popitem()
            query_kwargs = {query_field: query_value}
        try:
            user = get_user_model()._default_manager.get(**query_kwargs)
            if not next_kwargs:
                next_kwargs = {
                    "password": password,
                    get_user_model().USERNAME_FIELD: getattr(
                        user, get_user_model().USERNAME_FIELD
                    ),
                }
            if is_archived_user(user):
                user.is_active = True
                user.save()
            return cls.parent_resolve(root, info, **next_kwargs)
        except Exception:
            return cls(success=False, errors=Messages.INVALID_CREDENTIALS)


class VerifyOrRefreshOrRevokeTokenMixin(Output):
    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            return cls.parent_resolve(root, info, **kwargs)
        except (JSONWebTokenExpired, JSONWebTokenError):
            token_field_name = get_token_field_name(
                cls._meta.arguments
            ) or get_token_field_name(
                cls._meta.arguments["input"]._meta.fields, "token"
            )
            return cls(
                success=False, errors={token_field_name: Messages.INVALID_TOKEN}
            )


class SendEmailMixin:
    @classmethod
    def send_email(cls, info, user, email):
        token = get_token(user, cls.token_action)
        site = get_current_site(info.context)
        context = {
            "user": user,
            "token": token,
            "port": info.context.get_port(),
            "site_name": site.name,
            "domain": site.domain,
            "protocol": "https" if info.context.is_secure() else "http",
            "url": cls.url,
        }
        return cls.email_class.send(to=email, context=context)


class RegisterMixin(SendEmailMixin, Output):
    """
    Mutation to register a user
    """

    form = RegisterForm
    email_class = ActivationEmail
    token_action = TokenAction.ACTIVATION
    url = settings.ACTIVATION_URL_ON_EMAIL

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            f = cls.form(kwargs)
            if f.is_valid():
                user = f.save(commit=False)
                send_activation = (
                    settings.SEND_ACTIVATION_EMAIL == True and kwargs["email"]
                )
                user.is_active = False if send_activation else True
                if send_activation:
                    cls.send_email(info, user, kwargs["email"])

                user.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)


class UpdateAccountMixin(Output):
    """
    Update user models fields
    """

    form = UpdateAccountForm

    @classmethod
    @is_authenticated_and_verified
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        f = cls.form(kwargs, instance=user)
        if f.is_valid():
            f.save()
            return cls(success=True)
        else:
            return cls(success=False, errors=f.errors.get_json_data())


class UserEmailMixin:
    """
    Provide get user by email query and email form
    """

    @classmethod
    def get_user_by_email(cls, email):
        f = EmailForm({"email": email})
        if f.is_valid():
            # can raise ObjectDoesNotExist
            email_field_name = get_user_model().get_email_field_name()
            user = get_user_model()._default_manager.get(
                **{email_field_name: email}
            )
            return user
        else:
            return cls(success=False, errors=f.errors.get_json_data())


class ResendActivationEmailMixin(UserEmailMixin, SendEmailMixin, Output):
    """
    Mutation to resend an activation email
    """

    email_class = ResendActivationEmail
    token_action = TokenAction.ACTIVATION
    url = settings.ACTIVATION_URL_ON_EMAIL

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        email = kwargs.get("email")
        try:
            user = cls.get_user_by_email(email=email)
            if user.is_active:
                return cls(
                    success=False,
                    errors={"email": [Messages.ALREADY_VERIFIED]},
                )
            try:
                cls.send_email(info, user, email)
                return cls(success=True)
            except SMTPException:
                return cls(success=False, errors=Messages.EMAIL_FAIL)
        except ObjectDoesNotExist:
            # return true even if user is not registred
            return cls(success=True)
        return cls(success=True)


class VerifyAccountMixin(Output):
    """
    Mutation to verify user from email authentication
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        token = kwargs.get("token")
        try:
            payload = get_token_paylod(
                token,
                TokenAction.ACTIVATION,
                settings.EXPIRATION_ACTIVATION_TOKEN,
            )
            user = get_user_model()._default_manager.get(**payload)
            if not is_archived_user(user) and is_not_verified_user(user):
                user.is_active = True
                user.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=Messages.ALREADY_VERIFIED)
        except Exception:
            return cls(success=False, errors=Messages.INVALID_TOKEN)


class ArchiveOrDeleteMixin(Output):
    @classmethod
    @is_authenticated_and_verified
    @password_confirmation
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        cls.resolve_action(user)
        return cls(success=True)


class ArchiveAccountMixin(ArchiveOrDeleteMixin):
    """
    Mutation to archive account
    """

    @classmethod
    def resolve_action(cls, user):
        user.is_active = False
        user.save()


class DeleteAccountMixin(ArchiveOrDeleteMixin):
    """
    Mutation to delete account
    """

    @classmethod
    def resolve_action(cls, user):
        user.delete()


class RevokeRefreshTokenMixin(graphql_jwt.refresh_token.mixins.RevokeMixin):
    """
    Revoke refresh token on password change or password reset
    revoke only if:
    GRAPHQL_JWT['JWT_LONG_RUNNING_REFRESH_TOKEN'] is True
    """

    @classmethod
    def revoke_user_refresh_token(cls, root, info, user, should_revoke):
        if not should_revoke:
            return
        if hasattr(
            django_settings, "GRAPHQL_JWT"
        ) and django_settings.GRAPHQL_JWT.get(
            "JWT_LONG_RUNNING_REFRESH_TOKEN", False
        ):
            try:
                refresh_tokens = user.refresh_tokens.all()
                for refresh_token in refresh_tokens:
                    revoked = cls.revoke(root, info, refresh_token)
            except (JSONWebTokenExpired, JSONWebTokenError):
                pass


class PasswordChangeMixin(Output, RevokeRefreshTokenMixin):
    """
    Mutation to change account password
    """

    form = PasswordChangeForm

    @classmethod
    @is_authenticated_and_verified
    @password_confirmation
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        f = cls.form(user, kwargs)
        if f.is_valid():
            cls.revoke_user_refresh_token(
                root, info, user, settings.LOGOUT_ON_PASSWORD_CHANGE
            )
            user = f.save()
            return cls(success=True)
        else:
            return cls(success=False, errors=f.errors.get_json_data())


class SendPasswordResetEmailMixin(UserEmailMixin, SendEmailMixin, Output):
    """
    Mutation to send password reset email
    """

    email_class = PasswordResetEmail
    token_action = TokenAction.PASSWORD_RESET
    url = settings.PASSWORD_RESET_URL_ON_EMAIL

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        email = kwargs.get("email")
        try:
            user = cls.get_user_by_email(email=email)
            if is_not_verified_user(user):
                return cls(
                    success=False,
                    errors={"email": [Messages.NOT_VERIFIED_PASSWORD_RESET]},
                )
            try:
                cls.send_email(info, user, email)
                return cls(success=True)
            except SMTPException:
                return cls(success=False, errors=Messages.EMAIL_FAIL)
        except ObjectDoesNotExist:
            # return true even if user is not registred
            return cls(success=True)
        return cls(success=True)


class PasswordResetMixin(Output, RevokeRefreshTokenMixin):
    """
    Mutation to reset password
    """

    form = SetPasswordForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.pop("token")
            payload = get_token_paylod(
                token,
                TokenAction.PASSWORD_RESET,
                settings.EXPIRATION_PASSWORD_RESET_TOKEN,
            )
            user = get_user_model()._default_manager.get(**payload)
            f = cls.form(user, kwargs)
            if f.is_valid():
                cls.revoke_user_refresh_token(
                    root, info, user, settings.LOGOUT_ON_PASSWORD_RESET
                )
                user = f.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())
        except Exception:
            return cls(success=False, errors=Messages.INVALID_TOKEN)
