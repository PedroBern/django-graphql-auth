import graphene
from graphene_django.utils import camelize


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
