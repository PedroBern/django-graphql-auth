from django.contrib.auth import get_user_model

import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .settings import graphql_auth_settings as app_settings


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = app_settings.USER_NODE_FILTER_FIELDS
        exclude_fields = app_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (graphene.relay.Node,)

    pk = graphene.Int()
    archived = graphene.Boolean()
    verified = graphene.Boolean()
    secondary_email = graphene.String()

    def resolve_pk(self, info):
        return self.pk

    def resolve_archived(self, info):
        return self.status.archived

    def resolve_verified(self, info):
        return self.status.verified

    def resolve_secondary_email(self, info):
        return self.status.secondary_email


class UserQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class MeQuery(graphene.ObjectType):
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
