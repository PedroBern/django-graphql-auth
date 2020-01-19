# Installation

!!! info
    If you are not familiarized with
    [Graphene](https://github.com/graphql-python/graphene)
    or [GraphQL JWT](https://github.com/flavors/django-graphql-jwt), skip this
    installation section and go to the [quickstart](/quickstart) guide.

---

## Requirements

###### Supported versions of Django and Python

| Django / python |3.6|3.7|3.8|
| --- |:---:|:---:|:---:|
|2.1|x|x|x|
|2.2|x|x|x|
|3.0|x|x|x|

---

## Installation

```bash
pip install django-graphql-auth
```

!!! Note ""
    For those that are not installed, this will automatically install `graphene`, `graphene-django`,
    `django-graphql-jwt`, `django-filter` and `django`.

---

## Minimum setup

### 1. Email Templates

!!! Note ""
    Overriding email templates is covered [here](/overriding-email-templates).

If you plan to use the default email templates, add ``graphql_auth`` to your
installed apps.

```python
INSTALLED_APPS = [
    # ...

    # only if using default email templates
    # you can remove it later
    "graphql_auth"
]
```

And make sure your templates configuration has the following:

```python
TEMPLATES = [
    {
        # ...
        'APP_DIRS': True,
    },
]
```

### 2. Email Backend

The default configuration is to send activation email,
you can set it to ``False`` on your [settings](/settings),
but you still need an Email Backend
to password reset.

The quickest solution for development is to setup a [Console Email Backend](https://docs.djangoproject.com/en/3.0/topics/email/#console-backend), simply add the following to your ```settings.py```.

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Now all emails are sent to the standard output, instead of an actual email.

### 3. Schema

In your schema, add the following:

```python tab="GraphQL"

import graphene

from graphql_auth.schema import UserQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

    # django-graphql-jwt authentication
    # with some extra features
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
```

```python tab="Relay"

import graphene

from graphql_auth.schema import UserQuery
from graphql_auth import relay

class AuthRelayMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    update_account = relay.UpdateAccount.Field()
    resend_activation_email = relay.ResendActivationEmail.Field()
    archive_account = relay.ArchiveAccount.Field()
    delete_account = relay.DeleteAccount.Field()
    password_change = relay.PasswordChange.Field()
    send_password_reset_email = relay.SendPasswordResetEmail.Field()
    password_reset = relay.PasswordReset.Field()

    # django-graphql-jwt authentication
    # with some extra features
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(AuthRelayMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
```

### 4. Refresh Token <small>- optional but recommended</small>

Refresh tokens are optional and this package will work with the default token
from [Django GraphQL JWT](https://github.com/flavors/django-graphql-jwt).

But having refresh tokens enabled will allow to revoke user tokens when
the password is changed/reset and when the account becomes archived.

Follow the [offitial docs](https://django-graphql-jwt.domake.io/en/latest/refresh_token.html#long-running-refresh-tokens) or simply add the following to your ``settings.py``:

```python
INSTALLED_APPS = [
    # ...
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig'
]

GRAPHQL_JWT = {
    # ...
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
}
```

And remenber to migrate:

```bash
python manage.py migrate
```
