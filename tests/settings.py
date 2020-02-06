import os
import sys

templates_root_dir = os.path.abspath(
    os.path.split(os.path.split(__file__)[0])[0]
).replace("tests", "graphql_auth/templates")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "graphene_django",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "django_filters",
    "graphql_auth",
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

SECRET_KEY = "test"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "graphql_jwt.backends.JSONWebTokenBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [templates_root_dir],
        "OPTIONS": {},
    }
]

MIDDLEWARE = ["django.contrib.auth.middleware.AuthenticationMiddleware"]


GRAPHENE = {
    "SCHEMA": "schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_ALLOW_ANY_CLASSES": [
        # mutations
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail"
        # relay
        "graphql_auth.relay.Register",
        "graphql_auth.relay.VerifyAccount",
        "graphql_auth.relay.ResendActivationEmail",
        "graphql_auth.relay.SendPasswordResetEmail",
        "graphql_auth.relay.PasswordReset",
        "graphql_auth.relay.ObtainJSONWebToken",
        "graphql_auth.relay.VerifyToken",
        "graphql_auth.relay.RefreshToken",
        "graphql_auth.relay.RevokeToken",
        "graphql_auth.relay.VerifySecondaryEmail",
    ],
}

GRAPHQL_AUTH = {}
