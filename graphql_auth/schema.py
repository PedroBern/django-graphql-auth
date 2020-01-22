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

    archived = graphene.Boolean()
    verified = graphene.Boolean()

    def resolve_archived(self, info):
        return self.status.archived

    def resolve_verified(self, info):
        return self.status.verified


class UserQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
