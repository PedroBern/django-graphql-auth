import graphene
import graphql_jwt

from .bases import RelayMutationMixin, DynamicInputMixin
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
)
from .utils import normalize_fields
from .settings import graphql_auth_settings as app_settings
from .schema import UserNode


class Register(
    RelayMutationMixin,
    DynamicInputMixin,
    RegisterMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = normalize_fields(
        app_settings.REGISTER_MUTATION_FIELDS, ["password1", "password2",],
    )
    _inputs = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(
    RelayMutationMixin,
    DynamicInputMixin,
    VerifyAccountMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["token"]


class ResendActivationEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    ResendActivationEmailMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["email"]


class SendPasswordResetEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    SendPasswordResetEmailMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["email"]


class SendSecondaryEmailActivation(
    RelayMutationMixin,
    DynamicInputMixin,
    SendSecondaryEmailActivationMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["email", "password"]


class VerifySecondaryEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    VerifySecondaryEmailMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["token"]


class SwapEmails(
    RelayMutationMixin,
    DynamicInputMixin,
    SwapEmailsMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["password"]


class PasswordReset(
    RelayMutationMixin,
    DynamicInputMixin,
    PasswordResetMixin,
    graphene.ClientIDMutation,
):
    _required_inputs = ["token", "new_password1", "new_password2"]


class ObtainJSONWebToken(
    RelayMutationMixin,
    ObtainJSONWebTokenMixin,
    graphql_jwt.relay.JSONWebTokenMutation,
):

    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments["input"]._meta.fields.update(
            {"password": graphene.InputField(graphene.String, required=True)}
        )
        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments["input"]._meta.fields.update(
                {field: graphene.InputField(graphene.String)}
            )
        return super(graphql_jwt.relay.JSONWebTokenMutation, cls).Field(
            *args, **kwargs
        )


class ArchiveAccount(
    RelayMutationMixin,
    ArchiveAccountMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):

    _required_inputs = ["password"]


class DeleteAccount(
    RelayMutationMixin,
    DeleteAccountMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):

    _required_inputs = ["password"]


class PasswordChange(
    RelayMutationMixin,
    PasswordChangeMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):

    _required_inputs = ["old_password", "new_password1", "new_password2"]


class UpdateAccount(
    RelayMutationMixin,
    DynamicInputMixin,
    UpdateAccountMixin,
    graphene.ClientIDMutation,
):

    _inputs = app_settings.UPDATE_MUTATION_FIELDS


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
