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

print(templates_root_dir)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [templates_root_dir],
        "OPTIONS": {},
    }
]

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE = [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

GRAPHENE = {
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}
