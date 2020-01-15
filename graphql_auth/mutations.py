import graphene
import graphql_jwt

from .types import UserNode
from .settings import settings
from .mixins import (
    MutationMixin,
    ObtainJSONWebTokenMixin,
    DynamicArgsMixin,
    RegisterMixin,
    UpdateAccountMixin,
    ResendActivationEmailMixin,
    VerifyAccountMixin,
    ArchiveAccountMixin,
    DeleteAccountMixin,
    PasswordChangeMixin,
    SendPasswordResetEmailMixin,
    PasswordResetMixin,
    VerifyOrRefreshOrRevokeTokenMixin,
)


class ObtainJSONWebToken(
    MutationMixin, ObtainJSONWebTokenMixin, graphql_jwt.JSONWebTokenMutation,
):
    """
    Get token and allow access to user
    If user is archived, make it active
    """

    user = graphene.Field(UserNode)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({"password": graphene.String(required=True)})
        for field in settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments.update({field: graphene.String()})
        return super(graphql_jwt.JSONWebTokenMutation, cls).Field(
            *args, **kwargs
        )


class VerifyToken(
    MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Verify
):
    """
    Verify token mutation
    """


class RefreshToken(
    MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Refresh
):
    """
    Refresh token mutation
    """


class RevokeToken(
    MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Revoke
):
    """
    Revoke token mutation
    """


class Register(
    MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation,
):
    """
    Mutation to register a user
    """

    _required_args = settings.MUTATION_FIELDS_REGISTER + [
        "password1",
        "password2",
    ]


class UpdateAccount(
    MutationMixin, DynamicArgsMixin, UpdateAccountMixin, graphene.Mutation,
):
    """
        Update user models fields
    """

    _args = settings.MUTATION_FIELDS_UPDATE


class ResendActivationEmail(
    MutationMixin,
    DynamicArgsMixin,
    ResendActivationEmailMixin,
    graphene.Mutation,
):
    """
    Mutation to resend an activation email
    """

    _required_args = ["email"]


class VerifyAccount(
    MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation,
):
    """
    Mutation to verify user from email authentication
    """

    _required_args = ["token"]


class ArchiveAccount(
    MutationMixin, ArchiveAccountMixin, DynamicArgsMixin, graphene.Mutation,
):
    """
    Mutation to archive account
    """

    _required_args = ["password"]


class DeleteAccount(
    MutationMixin, DeleteAccountMixin, DynamicArgsMixin, graphene.Mutation,
):
    """
    Mutation to delete account
    """

    _required_args = ["password"]


class PasswordChange(
    MutationMixin, PasswordChangeMixin, DynamicArgsMixin, graphene.Mutation,
):
    """
    Mutation to delete account
    """

    _required_args = ["old_password", "new_password1", "new_password2"]


class PasswordReset(
    MutationMixin, PasswordResetMixin, DynamicArgsMixin, graphene.Mutation,
):
    """
    Mutation to delete account
    """

    _required_args = ["token", "new_password1", "new_password2"]


class SendPasswordResetEmail(
    MutationMixin,
    SendPasswordResetEmailMixin,
    DynamicArgsMixin,
    graphene.Mutation,
):
    """
    Mutation to send password reset email
    """

    _required_args = ["email"]
