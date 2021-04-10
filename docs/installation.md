# Installation

!!! attention
    If you are not familiarized with
    [Graphene](https://github.com/graphql-python/graphene)
    or [GraphQL JWT](https://github.com/flavors/django-graphql-jwt), skip this
    installation section and go to the [quickstart](quickstart.md) guide.

---

## Requirements

- Python: 3.6 - 3.7 - 3.8
- Django: 2.2 - 3.0

---

## Installation

```bash
pip install django-graphql-auth
```

!!! Note ""
    For those that are not installed, this will automatically install `graphene`, `graphene-django`,
    `django-graphql-jwt`, `django-filter` and `django`.

Add `graphql_auth` to installed apps.

```python
INSTALLED_APPS = [
    # ...
    "graphql_auth"
]
```

Migrate:

```bash
python manage.py migrate
```

---

## Setup

The following are the minimum steps required to get it running. It should not take more than 10 minutes.

---

### 1. Schema

In your schema, add the following:

```python tab="GraphQL"

import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
```

```python tab="Relay"

import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import relay

class AuthRelayMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    resend_activation_email = relay.ResendActivationEmail.Field()
    send_password_reset_email = relay.SendPasswordResetEmail.Field()
    password_reset = relay.PasswordReset.Field()
    password_set = relay.PasswordSet.Field() # For passwordless registration
    password_change = relay.PasswordChange.Field()
    update_account = relay.UpdateAccount.Field()
    archive_account = relay.ArchiveAccount.Field()
    delete_account = relay.DeleteAccount.Field()
    send_secondary_email_activation =  relay.SendSecondaryEmailActivation.Field()
    verify_secondary_email = relay.VerifySecondaryEmail.Field()
    swap_emails = relay.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthRelayMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
```

---

### 2. Allow Any Classes

On your `#!python GRAPHQL_JWT["JWT_ALLOW_ANY_CLASSES"]` setting, add the following:

```python tab="GraphQL"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}
```

```python tab="Relay"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
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
```

---

### 3. Authentication Backend <small>- optional</small>

Add the following to your `#!python AUTHENTICATION_BACKENDS`:

```python
AUTHENTICATION_BACKENDS = [
    # remove this
    # "graphql_jwt.backends.JSONWebTokenBackend",

    # add this
    "graphql_auth.backends.GraphQLAuthBackend",

    # ...
]
```

!!! attention "What's the difference from the graphql_jwt.backend?"
    We implement the same backend with only one difference:

    - It will not raise if you send a request with bad token to a class that is not on `#!python JWT_ALLOW_ANY_CLASSES`.

    ---

    Why should I want this behaivor?

    Intead of raising an actual error, we can handle it and return whatever make sense, e.g.:
    ```python
      cls(success=False errors="Unauthenticated.")
    ```

    ---

    You should handle this situation doing one of the following:

    - Simply use the graphql_jwt decorator [@login_required](https://django-graphql-jwt.domake.io/en/latest/decorators.html#login-required).
    - Use [our login_required decorator](https://github.com/PedroBern/django-graphql-auth/blob/fce93a3f6103d7194d3e3fbd28b7466602b8bf31/graphql_auth/decorators.py#L7), note that this expect your output to contain [this output](https://github.com/PedroBern/django-graphql-auth/blob/fce93a3f6103d7194d3e3fbd28b7466602b8bf31/graphql_auth/bases.py#L6).
    - Create your own login_required decorator!

---

### 4. Refresh Token <small>- optional</small>

Refresh tokens are optional and this package will work with the default token
from [Django GraphQL JWT](https://github.com/flavors/django-graphql-jwt).

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

And remember to migrate:

```bash
python manage.py migrate
```

---

### 5. Email Templates

!!! Note ""
    Overriding email templates is covered [here](overriding-email-templates.md).

This package comes with some default email templates, if you plan to use it, make sure your templates configuration has the following:

```python
TEMPLATES = [
    {
        # ...
        'APP_DIRS': True,
    },
]
```

---

### 6. Email Backend

The default configuration is to send activation email,
you can set it to ``False`` on your [settings](settings.md),
but you still need an Email Backend
to password reset.

The quickest way for development is to setup a [Console Email Backend](https://docs.djangoproject.com/en/3.0/topics/email/#console-backend), simply add the following to your ```settings.py```.

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Now all emails are sent to the standard output, instead of an actual email.

---
