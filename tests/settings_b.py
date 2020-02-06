from .settings import *

GRAPHQL_AUTH = {
    "ALLOW_DELETE_ACCOUNT": True,
    "REGISTER_MUTATION_FIELDS": {"email": "String", "username": "String"},
    "UPDATE_MUTATION_FIELDS": ["first_name", "last_name"],
    "ALLOW_LOGIN_NOT_VERIFIED": False,
}

INSTALLED_APPS += ["tests"]

AUTH_USER_MODEL = "tests.CustomUser"
