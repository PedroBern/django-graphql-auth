import graphene

from .bases import MutationMixin, DynamicArgsMixin
from .mixins import (
    RegisterMixin,
    VerifyAccountMixin,
    ResendActivationEmailMixin,
    SendPasswordResetEmailMixin,
    PasswordResetMixin,
)
from .utils import normalize_fields
from .settings import graphql_auth_settings as app_settings


class Register(
    MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation,
):
    _required_args = normalize_fields(
        app_settings.REGISTER_MUTATION_FIELDS, ["password1", "password2",],
    )
    _args = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(
    MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation
):
    _required_args = ["token"]


class ResendActivationEmail(
    MutationMixin,
    DynamicArgsMixin,
    ResendActivationEmailMixin,
    graphene.Mutation,
):
    _required_args = ["email"]


class SendPasswordResetEmail(
    MutationMixin,
    DynamicArgsMixin,
    SendPasswordResetEmailMixin,
    graphene.Mutation,
):
    _required_args = ["email"]


class PasswordReset(
    MutationMixin, DynamicArgsMixin, PasswordResetMixin, graphene.Mutation
):
    _required_args = ["token", "new_password1", "new_password2"]
