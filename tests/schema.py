import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
import graphql_jwt

from graphql_auth.types import UserNodeRelay, UserNode
from graphql_auth import relay
from graphql_auth import mutations


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


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


class UserRelayQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNodeRelay)
    users = DjangoFilterConnectionField(UserNodeRelay)


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


class RelayQuery(UserRelayQuery, graphene.ObjectType):
    pass


class RelayMutation(AuthRelayMutation, graphene.ObjectType):
    pass


relay_schema = graphene.Schema(query=RelayQuery, mutation=RelayMutation)


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


default_schema = graphene.Schema(query=Query, mutation=Mutation)
