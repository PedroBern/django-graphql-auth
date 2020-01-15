import graphene
import graphql_jwt

from .utils import resolve_fields
from .settings import graphql_auth_settings as settings
from .types import UserNodeRelay
from .mixins import (
    RelayMutationMixin,
    ObtainJSONWebTokenMixin,
    DynamicInputMixin,
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
    RelayMutationMixin,
    ObtainJSONWebTokenMixin,
    graphql_jwt.relay.JSONWebTokenMutation,
):
    """
    Get token and allow access to user
    If user is archived, make it active
    """

    user = graphene.Field(UserNodeRelay)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments["input"]._meta.fields.update(
            {"password": graphene.InputField(graphene.String, required=True)}
        )
        for field in settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments["input"]._meta.fields.update(
                {field: graphene.InputField(graphene.String)}
            )
        return super(graphql_jwt.relay.JSONWebTokenMutation, cls).Field(
            *args, **kwargs
        )


class VerifyToken(
    RelayMutationMixin,
    VerifyOrRefreshOrRevokeTokenMixin,
    graphql_jwt.relay.Verify,
):
    """
    Verify token mutation
    """

    class Input:
        token = graphene.String(required=True)


class RefreshToken(
    RelayMutationMixin,
    VerifyOrRefreshOrRevokeTokenMixin,
    graphql_jwt.relay.Refresh,
):
    """
    Refresh token mutation
    """

    class Input(graphql_jwt.mixins.RefreshMixin.Fields):
        """Refresh Input"""


class RevokeToken(
    RelayMutationMixin,
    VerifyOrRefreshOrRevokeTokenMixin,
    graphql_jwt.relay.Revoke,
):
    """
    Revoke token mutation
    """

    class Input:
        refresh_token = graphene.String(required=True)


class Register(
    RelayMutationMixin,
    DynamicInputMixin,
    RegisterMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to register a user
    """

    _required_inputs = resolve_fields(
        settings.REGISTER_MUTATION_FIELDS, ["password1", "password2",]
    )
    _inputs = settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class UpdateAccount(
    RelayMutationMixin,
    DynamicInputMixin,
    UpdateAccountMixin,
    graphene.ClientIDMutation,
):
    """
        Update user models fields
    """

    _inputs = settings.UPDATE_MUTATION_FIELDS


class ResendActivationEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    ResendActivationEmailMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to resend an activation email
    """

    _required_inputs = ["email"]


class VerifyAccount(
    RelayMutationMixin,
    DynamicInputMixin,
    VerifyAccountMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to verify user from email authentication
    """

    _required_inputs = ["token"]


class ArchiveAccount(
    RelayMutationMixin,
    ArchiveAccountMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to archive account
    """

    _required_inputs = ["password"]


class DeleteAccount(
    RelayMutationMixin,
    DeleteAccountMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to delete account
    """

    _required_inputs = ["password"]


class PasswordChange(
    RelayMutationMixin,
    PasswordChangeMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to delete account
    """

    _required_inputs = ["old_password", "new_password1", "new_password2"]


class PasswordReset(
    RelayMutationMixin,
    PasswordResetMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to delete account
    """

    _required_inputs = ["token", "new_password1", "new_password2"]


class SendPasswordResetEmail(
    RelayMutationMixin,
    SendPasswordResetEmailMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    """
    Mutation to send password reset email
    """

    _required_inputs = ["email"]
