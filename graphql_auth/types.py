import json

from django.contrib.auth import get_user_model

from graphene import relay
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.utils import camelize

from .settings import settings


class UserNode(DjangoObjectType):
    """
    User Node
    """

    class Meta:
        model = get_user_model()
        filter_fields = settings.USER_NODE_FILTER_FIELDS
        exclude_fields = settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (graphene.Node,)


class UserNodeRelay(UserNode):
    """
    User Node
    """

    class Meta:
        model = get_user_model()
        filter_fields = settings.USER_NODE_FILTER_FIELDS
        exclude_fields = settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (relay.Node,)


class ErrorType(graphene.Scalar):
    class Meta:
        description = """
    Errors messages and codes mapped to
    fields or non fields errors.

    Example:
    {
        field_name: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        other_field: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        nonFieldErrors: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ]
    }
    """

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if hasattr(errors, "__all__"):
                errors["non_field_errors"] = errors.__all__
            return camelize(errors)
        elif isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise Exception("`errors` must be list or dict!")

    # @staticmethod
    # def parse_literal(node):
    #     return node.value
    #
    # @staticmethod
    # def parse_value(value):
    #     return value
