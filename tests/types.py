import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)
        skip_registry = True

    pk = graphene.Int()
    verified = graphene.Boolean()

    def resolve_pk(self, info):
        return self.pk

    def resolve_verified(self, info):
        return self.status.verified
