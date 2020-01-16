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
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "django_filters",
    "graphql_auth",
]

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3",},
}

SECRET_KEY = "test"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "graphql_jwt.backends.JSONWebTokenBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [templates_root_dir],
        "OPTIONS": {},
    }
]

MIDDLEWARE = [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]


GRAPHENE = {
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

GRAPHQL_JWT = {
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
}
