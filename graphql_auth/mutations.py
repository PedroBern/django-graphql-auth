import graphene
import graphql_jwt

from .bases import MutationMixin, DynamicArgsMixin
from .mixins import (
    RegisterMixin,
    VerifyAccountMixin,
    ResendActivationEmailMixin,
    SendPasswordResetEmailMixin,
    PasswordResetMixin,
    ObtainJSONWebTokenMixin,
    ArchiveAccountMixin,
    DeleteAccountMixin,
    PasswordChangeMixin,
    UpdateAccountMixin,
    VerifyOrRefreshOrRevokeTokenMixin,
    SendSecondaryEmailActivationMixin,
    VerifySecondaryEmailMixin,
    SwapEmailsMixin,
    RemoveSecondaryEmailMixin,
)
from .utils import normalize_fields
from .settings import graphql_auth_settings as app_settings
from .schema import UserNode


class Register(MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation):

    __doc__ = RegisterMixin.__doc__
    _required_args = normalize_fields(
        app_settings.REGISTER_MUTATION_FIELDS, ["password1", "password2"]
    )
    _args = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(
    MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation
):
    __doc__ = VerifyAccountMixin.__doc__
    _required_args = ["token"]


class ResendActivationEmail(
    MutationMixin, DynamicArgsMixin, ResendActivationEmailMixin, graphene.Mutation
):
    __doc__ = ResendActivationEmailMixin.__doc__
    _required_args = ["email"]


class SendPasswordResetEmail(
    MutationMixin, DynamicArgsMixin, SendPasswordResetEmailMixin, graphene.Mutation
):
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_args = ["email"]


class SendSecondaryEmailActivation(
    MutationMixin,
    DynamicArgsMixin,
    SendSecondaryEmailActivationMixin,
    graphene.Mutation,
):
    __doc__ = SendSecondaryEmailActivationMixin.__doc__
    _required_args = ["email", "password"]


class VerifySecondaryEmail(
    MutationMixin, DynamicArgsMixin, VerifySecondaryEmailMixin, graphene.Mutation
):
    __doc__ = VerifySecondaryEmailMixin.__doc__
    _required_args = ["token"]


class SwapEmails(MutationMixin, DynamicArgsMixin, SwapEmailsMixin, graphene.Mutation):
    __doc__ = SwapEmailsMixin.__doc__
    _required_args = ["password"]


class RemoveSecondaryEmail(
    MutationMixin, DynamicArgsMixin, RemoveSecondaryEmailMixin, graphene.Mutation
):
    __doc__ = RemoveSecondaryEmailMixin.__doc__
    _required_args = ["password"]


class PasswordReset(
    MutationMixin, DynamicArgsMixin, PasswordResetMixin, graphene.Mutation
):
    __doc__ = PasswordResetMixin.__doc__
    _required_args = ["token", "new_password1", "new_password2"]


class ObtainJSONWebToken(
    MutationMixin, ObtainJSONWebTokenMixin, graphql_jwt.JSONWebTokenMutation
):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({"password": graphene.String(required=True)})
        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments.update({field: graphene.String()})
        return super(graphql_jwt.JSONWebTokenMutation, cls).Field(*args, **kwargs)


class ArchiveAccount(
    MutationMixin, ArchiveAccountMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = ArchiveAccountMixin.__doc__
    _required_args = ["password"]


class DeleteAccount(
    MutationMixin, DeleteAccountMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = DeleteAccountMixin.__doc__
    _required_args = ["password"]


class PasswordChange(
    MutationMixin, PasswordChangeMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = PasswordChangeMixin.__doc__
    _required_args = ["old_password", "new_password1", "new_password2"]


class UpdateAccount(
    MutationMixin, DynamicArgsMixin, UpdateAccountMixin, graphene.Mutation
):
    __doc__ = UpdateAccountMixin.__doc__
    _args = app_settings.UPDATE_MUTATION_FIELDS


class VerifyToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Verify):
    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__


class RefreshToken(
    MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Refresh
):
    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__


class RevokeToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Revoke):
    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__
