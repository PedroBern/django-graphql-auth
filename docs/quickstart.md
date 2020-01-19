# Quickstart

---

## What to expect

- Fully functional API to handle user account
- Both graphQL and Relay versions

---

## Start a new Django Project <small>- optional</small>

!!! info ""
    It's recommended to use [virtual env wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html) or [virtualenv](https://virtualenv.pypa.io/en/latest/) to create
    your project inside an isolated python environment. We will use the first.

### Create the virtual env

```bash
mkvirtualenv graphql-auth-quickstart
```

### Create the Django Project

First install django:

```bash
pip install django
```

Then, create the new project:

```bash
django-admin startproject project
cd project
python manage.py migrate
```

Open the new folder on you favorite text editor, I like [Atom](https://atom.io/).

```bash
atom .
```

---

## Setup Graphene and GraphQL JWT

??? Question "What is Graphene-Django?"
    [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/)
    "make it easy to add GraphQL functionality to your Django project".

??? Question "What is Django-GraphQL-JWT?"
    [Django-GraphQL-JWT](https://django-graphql-jwt.domake.io/en/latest/index.html)
    is the easiest way to add JSON Web token authentication for Django with GraphQL.

!!! info ""
    The following instructions are the shameless copy of the
    [Graphene Django installation](https://docs.graphene-python.org/projects/django/en/latest)
    and the [Django GraphQL JWT quickstart](https://django-graphql-jwt.domake.io/en/latest/index.html).

### Installation

```bash
pip install graphene-django django-graphql-jwt
```

### Add the url

```python
# project.urls.py

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

urlpatterns = [
    # ...
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
```

### Edit your settings

```python
# project.settings.py

INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles', # Required for GraphiQL
    'graphene_django'


    # refresh tokens are optional, but recommended
    # to allow to revoke user tokens when password change/reset
    # or account is archived.
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',

    ''
]

MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ...
]

GRAPHENE = {
    'SCHEMA': 'project.schema.schema', # this file doesn't exist yet
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,

    # optional, explained in the INSTALLED_APPS
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
}
```

If you choose to use the refresh tokens, remenber to migrate:

```bash
python manage.py migrate
```

---

## Install Django-GraphQL-Auth

```bash
pip install django-graphql-auth
```

```python
# settings.py

INSTALLED_APPS = [
   # ...

   # just to load default email templates
   # when we override the templates, this can be removed
   "graphql_auth",
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

---

## Query


### Create the schema

Create a file called ``schema.py`` next to your ``settings.py`` with the following:

```python
# project.schema.py

import graphene

from graphql_auth.schema import UserQuery

class Query(UserQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
```

And add [Django-Filter](https://django-filter.readthedocs.io/en/master/index.html)
to the installed apps.

!!! info ""
    ``django-filter`` was automatically installed when you installed ``django-graphql-auth``.

```python
INSTALLED_APPS = [
    # ...
    'django_filters'
]
```

### Load fixtures

Before starting to query, let's load some users on the database. Create a new file
called ``users.json`` in the same directory as ``manage.py`` with the following:

```json
[
  {
      "model": "auth.user",
      "pk": 1,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": true,
          "username": "admin",
          "first_name": "",
          "last_name": "",
          "email": "admin@email.com",
          "is_staff": true,
          "is_active": true
      }
  },
  {
      "model": "auth.user",
      "pk": 2,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": false,
          "username": "active_user",
          "first_name": "",
          "last_name": "",
          "email": "active_user@email.com",
          "is_staff": false,
          "is_active": true
      }
  },
  {
      "model": "auth.user",
      "pk": 3,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": false,
          "username": "inactive_user",
          "first_name": "",
          "last_name": "",
          "email": "inactive_user@email.com",
          "is_staff": false,
          "is_active": false
      }
  }
]
```

run:

```bash
python manage.py loaddata users.json
```

### Making your first query

Start the dev server:

```bash
python manage.py runserver
```

Open your browser:

```bash
http://127.0.0.1:8000/graphql
```

!!! info ""
    This will open the [GraphiQL API browser](https://github.com/graphql/graphiql),
    where you can play with your queries and mutations, also let you explore the schema.

Copy the query below, paste on the GraphiQL interface and hit the play button.

```tab="query"
query {
  users {
    edges {
      node {
        username
      }
    }
  }
}
```

```tab="response"
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "username": "admin"
          }
        },
        {
          "node": {
            "username": "active_user"
          }
        },
        {
          "node": {
            "username": "inactive_user"
          }
        }
      ]
    }
  }
}
```

!!! info ""
    Note the ``edges`` and ``node``. The ``UserQuery`` uses relay to enable
    the filtering of ``django-filter``.

### Query with filters

The ``UserQuery`` comes with some default filters:

```tab="query"
query {
  users (isActive: true, username_Icontains: "user") {
    edges {
      node {
        id,
        username,
        isActive
      }
    }
  }
}
```

```tab="response"
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "id": "VXNlck5vZGU6Mg==",
            "username": "active_user",
            "isActive": true
          }
        }
      ]
    }
  }
}
```

Take a minute to explore the GraphiQL API browser and query schema on the right upper
corner under docs tab.

---

## Setup Email Backend

The default configuration is to send activation email when registring users,
you can set it to ``False`` on your [settings](/settings),
but you still need an Email Backend
to password reset.

The quickest solution for development is to setup a [Console Email Backend](https://docs.djangoproject.com/en/3.0/topics/email/#console-backend), simply add the following to your ```settings.py```.

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Now all emails are sent to the standard output, instead of an actual email and we
are ready to continue this guide.

---

## Mutations

Now let's add some mutations to our schema, starting with the registration. On
the ``schema.py`` add the following:

### Register

```python tab="mutations" hl_lines="6 8 9 14 15 17"
# project.schema.py

import graphene

from graphql_auth.schema import UserQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

```python tab="relay" hl_lines="6 8 9 14 15 17"
# project.schema.py

import graphene

from graphql_auth.schema import UserQuery
from graphql_auth import relay

class AuthMutation(graphene.ObjectType):
   register = relay.Register.Field()

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

Take a minute to explore the schema on the documentation tab again.

Let's try to register a new user:

```python tab="graphql"
mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password1: "123456",
    password2: "123456",
  ) {
    success,
    errors
  }
}
```

```python tab="response"
{
  "data": {
    "register": {
      "success": false,
      "errors": {
        "password2": [
          {
            "message": "This password is too short. It must contain at least 8 characters.",
            "code": "password_too_short"
          },
          {
            "message": "This password is too common.",
            "code": "password_too_common"
          },
          {
            "message": "This password is entirely numeric.",
            "code": "password_entirely_numeric"
          }
        ]
      }
    }
  }
}
```

```python tab="relay" hl_lines="3 8"
mutation {
  register(
    input: {
      email: "new_user@email.com",
      username: "new_user",
      password1: "123456",
      password2: "123456",
    }
  ) {
    success,
    errors
  }
}
```

Something went wrong! Now you know the response format that you can expect of
all mutations.

Let's try again:

```python tab="graphql"
mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password1: "supersecretpassword",
    password2: "supersecretpassword",
  ) {
    success,
    errors
  }
}
```

```python tab="response"
{
  "data": {
    "register": {
      "success": true,
      "errors": null
    }
  }
}
```

```python tab="relay" hl_lines="3 8"
mutation {
  register(
    input: {
      email: "new_user@email.com",
      username: "new_user",
      password1: "supersecretpassword",
      password2: "supersecretpassword",
    }
  ) {
    success,
    errors
  }
}
```

Check if the new user is really on the database:

```tab="query"
query {
  users (last: 1){
    edges {
      node {
        id,
        username,
        isActive
      }
    }
  }
}
```

```tab="response" hl_lines="8"
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "id": "VXNlck5vZGU6NA==",
            "username": "new_user",
            "isActive": false
          }
        }
      ]
    }
  }
}
```

There is actually a new user, but it is not active yet. We still need to activate the account.

Save the ``id`` of the new user, so we can query it later.

Go to your console and note the email that has been sent. Should be two outputs,
html and plain text formats.

Save the token from the url, something like this:

```bash
eyJ1c2VybmFtZSI6Im5ld191c2VyIiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1isoSr:CDwK_fjBSxWj3adC-X16wqzv-Mw
```

### Account Verification

Add the following to the ``AuthMutation``:

```python tab="graphql" hl_lines="5"
# schema.py

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
```

```python tab="relay" hl_lines="5"
# schema.py

class AuthMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
```

Take a minute again to see the changes on your schema.

Run the follow on your browser:

```python tab="graphql"
mutation {
  verifyAccount(token: "YOUR TOKEN HERE") {
    success,
    errors
  }
}
```

```python tab="response"
{
  "data": {
    "verifyAccount": {
      "success": true,
      "errors": null
    }
  }
}
```

```python tab="relay" hl_lines="3 5"
mutation {
  verifyAccount(
    input: {
      token: "YOUR TOKEN HERE"
    }
  )
  {
    success,
    errors
  }
}
```

Check if the user is active now, using the id that you saved early:

```tab="query"
query {
  user (id: "VXNlck5vZGU6NA=="){
    username,
    isActive
  }
}
```

```tab="response" hl_lines="5"
{
  "data": {
    "user": {
      "username": "new_user",
      "isActive": true
    }
  }
}
```

---

## Next steps

- Add all mutations to your schema!
- Navigate through the GraphiQL Documentation Explorer.
- Change the [settings](/settings).
- Explore the [api](/api).
- [Override email templates]("/overriding-email-templates").
- Explore [these useful links](/community).

### Full schema

```python tab="GraphQL" hl_lines="4 5 6 7 8 9 10 14 15 16 17"
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
```

```python tab="Relay" hl_lines="4 5 6 7 8 9 10 14 15 16 17"
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
```
