import graphene
import graphql_jwt
from graphene_django.filter.fields import DjangoFilterConnectionField

from graphql_auth import mutations, relay
from graphql_auth.schema import MeQuery, UserQuery

from .types import UserType


class PublicUserQuery(graphene.ObjectType):
    public_user = graphene.Field(UserType)

    def resolve_public_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None


class AuthMutation(graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()


class AuthRelayMutation(graphene.ObjectType):
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    update_account = relay.UpdateAccount.Field()
    resend_activation_email = relay.ResendActivationEmail.Field()
    archive_account = relay.ArchiveAccount.Field()
    delete_account = relay.DeleteAccount.Field()
    password_change = relay.PasswordChange.Field()
    send_password_reset_email = relay.SendPasswordResetEmail.Field()
    password_reset = relay.PasswordReset.Field()
    password_set = relay.PasswordSet.Field()
    verify_secondary_email = relay.VerifySecondaryEmail.Field()
    swap_emails = relay.SwapEmails.Field()
    remove_secondary_email = relay.RemoveSecondaryEmail.Field()
    send_secondary_email_activation = relay.SendSecondaryEmailActivation.Field()


class Query(UserQuery, MeQuery, PublicUserQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


class RelayMutation(AuthRelayMutation, graphene.ObjectType):
    pass


relay_schema = graphene.Schema(query=Query, mutation=RelayMutation)
default_schema = graphene.Schema(query=Query, mutation=Mutation)
