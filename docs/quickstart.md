# Quickstart

---

## What to expect

- Fully functional API to handle user account
- Both graphQL and Relay versions
- Setup with custom user model
- 20 to 30 minutes

[Final code on github](https://github.com/PedroBern/django-graphql-auth/tree/master/quickstart).

---

## Start a new Django Project

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
django-admin startproject quickstart
cd quickstart
```

### Create the custom user model

Changing to a custom user model mid-project is significantly more difficult. So let's start by adding it now. Run the following:

```bash
python manage.py startapp users
```

Then, create the custom user model:

```python
# users/models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
  
    USERNAME_FIELD = "username"   # e.g: "username", "email"
    EMAIL_FIELD = "email"         # e.g: "email", "primary_email"
```

Add it to the settings:

```python
# quickstart/settings.py

INSTALLED_APPS = [
    # ...
    'users'
]

AUTH_USER_MODEL = 'users.CustomUser'
```

Finally, migrate:

```bash
python manage.py migrate
```

!!! info ""
    You can customize the mutations to match your custom user model fields, see the [dynamic-fields settings](settings.md).

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
pip install graphene-django django-graphql-jwt==0.3.0
```

!!! info ""
    This package uses the 0.3.0 version of the django-graphql-jwt. We are working on to support the new 0.3.1 version. You can check the progress [here](https://github.com/PedroBern/django-graphql-auth/issues/23).

### Add the url

```python
# quickstart.urls.py

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
# quickstart.settings.py

INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles', # Required for GraphiQL
    'graphene_django',

    # refresh tokens are optional
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
]

MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ...
]

GRAPHENE = {
    'SCHEMA': 'quickstart.schema.schema', # this file doesn't exist yet
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

    # optional
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
}
```

If you choose to use the refresh tokens, remember to migrate:

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
   "graphql_auth",
]

AUTHENTICATION_BACKENDS = [
    # remove this
    # "graphql_jwt.backends.JSONWebTokenBackend",

    # add this
    "graphql_auth.backends.GraphQLAuthBackend",

    # ...
]
```

[Here](installation.md#3-authentication-backend-optional) is an explanation why we are adding this backend.

And make sure your templates configuration has the following:

```python
TEMPLATES = [
    {
        # ...
        'APP_DIRS': True,
    },
]
```

Run:

```bash
python manage.py migrate
```


---

## Query


### Create the schema

Create a file called ``schema.py`` next to your ``settings.py`` with the following:

```python
# quickstart.schema.py

import graphene

from graphql_auth.schema import UserQuery, MeQuery

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
```

Note: you can choose not to include ``UserQuery`` or ``MeQuery`` depending on your use case.

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

Before starting to query, let's load some users on the database. Create a new file called ``users.json`` in the same directory as ``manage.py`` with the following:

!!! info ""
    Have a look on the fixtures, note that we are creating 4 users and 3 `UserStatus`. When creating a user, we create a relating `UserStatus` by default on `post_save` signal with the following fields:

    ```python
    verified=False
    archived=False
    secondary_email=None
    ```

    You can access it on any user:

    ```bash
    user.status.[verified | archived | secondary_email]
    ```

```json
[
  {
      "model": "users.CustomUser",
      "pk": 1,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": false,
          "username": "user1",
          "first_name": "",
          "last_name": "",
          "email": "user1@email.com",
          "is_staff": false,
          "is_active": true
      }
  },
  {
      "model": "users.CustomUser",
      "pk": 2,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": false,
          "username": "user2",
          "first_name": "",
          "last_name": "",
          "email": "user2@email.com",
          "is_staff": false,
          "is_active": true
      }
  },
  {
      "model": "graphql_auth.userstatus",
      "pk": 2,
      "fields": {
          "user": 2,
          "verified": true,
          "archived": false,
          "secondary_email": null
      }
  },
  {
      "model": "users.CustomUser",
      "pk": 3,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": false,
          "username": "user3",
          "first_name": "",
          "last_name": "",
          "email": "user3@email.com",
          "is_staff": false,
          "is_active": true
      }
  },
  {
      "model": "graphql_auth.userstatus",
      "pk": 3,
      "fields": {
          "user": 3,
          "verified": true,
          "archived": true,
          "secondary_email": null
      }
  },
  {
      "model": "users.CustomUser",
      "pk": 4,
      "fields": {
          "password": "pbkdf2_sha256$180000$nFcBtiqGnWN9$hf58wNg77oT1BlNKRdATVVvBIa69+dz22fL1JKOKTaA=",
          "last_login": null,
          "is_superuser": false,
          "username": "user4",
          "first_name": "",
          "last_name": "",
          "email": "user4@email.com",
          "is_staff": false,
          "is_active": true
      }
  },
  {
      "model": "graphql_auth.userstatus",
      "pk": 4,
      "fields": {
          "user": 4,
          "verified": true,
          "archived": false,
          "secondary_email": "user4_secondary@email.com"
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
        username,
        archived,
        verified,
        email,
        secondaryEmail,
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
            "username": "user1",
            "archived": false,
            "verified": false,
            "email": "user1@email.com",
            "secondaryEmail": null
          }
        },
        {
          "node": {
            "username": "user2",
            "archived": false,
            "verified": true,
            "email": "user2@email.com",
            "secondaryEmail": null
          }
        },
        {
          "node": {
            "username": "user3",
            "archived": true,
            "verified": true,
            "email": "user3@email.com",
            "secondaryEmail": null
          }
        },
        {
          "node": {
            "username": "user4",
            "archived": false,
            "verified": true,
            "email": "user4@email.com",
            "secondaryEmail": "user4_secondary@email.com"
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
  users(status_Archived: true){
    edges {
      node {
        username,
        archived,
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
            "username": "user3",
            "archived": true
          }
        }
      ]
    }
  }
}
```

Take a minute to explore the GraphiQL API browser and query schema on the right upper
corner under docs tab.

### MeQuery

With ``MeQuery`` you can retrieve data for the currently authenticated user:

```tab="query"
query {
  me {
    username,
    verified
  }
}
```

```tab="response"
{
  "data": {
    "user": {
      "username": "new_user",
      "verified": true
    }
  }
}
```

Since this query requires an authenticated user it can only be explored by using the [insomnia API client](https://insomnia.rest/). See the below for more on how to use Insomnia.

---

## Setup Email Backend

The default configuration is to send activation email when registring users,
you can set it to ``False`` on your [settings](settings.md),
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

Now let's add some mutations to our schema, starting with the registration. On the ``schema.py`` add the following:

### Register

```python tab="mutations" hl_lines="6 8 9 14 15 17"
# quickstart.schema.py

import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

```python tab="relay" hl_lines="6 8 9 14 15 17"
# quickstart.schema.py

import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import relay

class AuthMutation(graphene.ObjectType):
   register = relay.Register.Field()

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

Take a minute to explore the schema on the documentation tab again.

On your `#!python GRAPHQL_JWT["JWT_ALLOW_ANY_CLASSES"]` setting, add the following:

```python tab="GraphQL"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
    ],
}
```

```python tab="Relay"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.relay.Register",
    ],
}
```

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
    errors,
    token,
    refreshToken
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
      },
      "token": null,
      "refreshToken": null
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
    errors,
    token,
    refreshToken
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
    errors,
    token,
    refreshToken
  }
}
```

```python tab="response"
{
  "data": {
    "register": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5ld191c2VyMjIiLCJleHAiOjE1ODAxMzUyMTQsIm9yaWdJYXQiOjE1ODAxMzQ5MTR9.lzMjYo_1LO-TMDotySi1VHoC5yLyKr5PWC2l-hdzQ20",
      "refreshToken": "8db1c55b8dbc1f4a24eabe6f5d44dc091a8ca0f7"
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
    errors,
    token,
    refreshToken
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
        email,
        isActive,
        archived,
        verified,
        secondaryEmail
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
            "id": "VXNlck5vZGU6NQ==",
            "username": "new_user",
            "email": "new_user@email.com",
            "isActive": true,
            "archived": false,
            "verified": false,
            "secondaryEmail": null
          }
        }
      ]
    }
  }
}
```

There is actually a new user and it is possible to log in (you can change it on the [settings](settings.md)),
but it is not verified yet.

Save the ``id`` of the new user, so we can query it later.

Go to your console and note the email that has been sent. Should be two outputs, html and plain text formats.

Save the token from the url, something like this:

```bash
eyJ1c2VybmFtZSI6Im5ld191c2VyIiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1isoSr:CDwK_fjBSxWj3adC-X16wqzv-Mw
```

---

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

On your `#!python GRAPHQL_JWT["JWT_ALLOW_ANY_CLASSES"]` setting, add the following:

```python tab="GraphQL" hl_lines="5"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
    ],
}
```

```python tab="Relay" hl_lines="5"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.relay.Register",
        "graphql_auth.relay.VerifyAccount",
    ],
}
```

Let's try to verify the account:

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
      token: "<YOUR TOKEN HERE>"
    }
  )
  {
    success,
    errors
  }
}
```

Check if the user is verified using the id that you have saved early:

```tab="query"
query {
  user (id: "<USER ID>"){
    username,
    verified
  }
}
```

```tab="response" hl_lines="5"
{
  "data": {
    "user": {
      "username": "new_user",
      "verified": true
    }
  }
}
```

---

### Login

Add the following to the ``AuthMutation``:

```python tab="graphql" hl_lines="6"
# schema.py

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
```

```python tab="relay" hl_lines="6"
# schema.py

class AuthMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    token_auth = relay.ObtainJSONWebToken.Field()
```

And again, on your `#!python GRAPHQL_JWT["JWT_ALLOW_ANY_CLASSES"]` setting, add the following:

```python tab="GraphQL" hl_lines="6"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ObtainJSONWebToken",
    ],
}
```

```python tab="Relay" hl_lines="6"
GRAPHQL_JWT = {
    #...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.relay.Register",
        "graphql_auth.relay.VerifyAccount",
        "graphql_auth.relay.ObtainJSONWebToken",
    ],
}
```

Let's try to login:

```python tab="graphql"
mutation {
  tokenAuth(username: "new_user", password: "supersecretpassword") {
    success,
    errors,
    unarchiving,
    token,
    refreshToken,
    unarchiving,
    user {
      id,
      username,
    }
  }
}
```

```python tab="response"
{
  "data": {
    "tokenAuth": {
      "success": true,
      "errors": null,
      "unarchiving": false,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5ld191c2VyIiwiZXhwIjoxNTc5ODk2Njc0LCJvcmlnSWF0IjoxNTc5ODk2Mzc0fQ.pNOkAWPyIanQWrKwvntQqf6asa8pkLuldW12N9nbfOo",
      "refreshToken": "fc1cf50178b7e7923e9580ff73920a04cfeaa9e7",
      "user": {
        "id": "VXNlck5vZGU6NQ==",
        "username": "new_user"
      }
    }
  }
}
```

```python tab="relay" hl_lines="3 6"
mutation {
  tokenAuth(
    input: {
      username: "new_user",
      password: "supersecretpassword"
    }
  ) {
    success,
    errors,
    unarchiving,
    token,
    refreshToken,
    unarchiving,
    user {
      id,
      username,
    }
  }
}
```

Save this `token`, we are going to use it to do some protected actions.

The GraphiQL interface that comes with Graphene is great! But to try all features, we need to send this token on the header and the GraphiQL do not support this.

---

### Insomnia API client

We are going to use [insomnia API client](https://insomnia.rest/) to send request with authorization header. It is really easy to setup, simple follow the instructions on the site.

Install and come back here!

---

### Update Account

This is the first mutation with login required that we are going to test.

Add the following to the ``AuthMutation``:

```python tab="graphql" hl_lines="7"
# schema.py

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
```

```python tab="relay" hl_lines="7"
# schema.py

class AuthMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    token_auth = relay.ObtainJSONWebToken.Field()
    update_account = relay.UpdateAccount.Field()
```

On the insomnia, create a new request and call it `updateAccount`. Select the method `POST`.

On the top of the window, add your graphql url:

```bash
http://127.0.0.1:8000/graphql
```

For the body, select `GraphQL Query`. Now it works exaclty as the graphiQL.

On the headers pane, create a new header:

- name: `Authorization`
- value: `JWT <TOKEN FROM THE LOGIN>`

Make the query:

```python tab="graphql"
mutation {
  updateAccount(
    firstName: "Joe"
  ) {
    success,
    errors
  }
}
```

```python tab="response"
{
  "data": {
    "updateAccount": {
      "success": true,
      "errors": null
    }
  }
}
```

```python tab="relay" hl_lines="3 5"
mutation {
  updateAccount(
    input: {
      firstName: "Joe"
    }
  ) {
    success,
    errors
  }
}
```

!!! tip ""
    If it fails because of the token (in case you took some time and it has expired), make the login again and get a new token.

Check if it worked:

```python tab="graphql"
query {
  user (id: "<USER ID>"){
    username,
    firstName
  }
}
```

```python tab="response"
{
  "data": {
    "user": {
      "username": "new_user",
      "firstName": "Joe"
    }
  }
}
```

---

## Next steps

- Add all mutations to your schema! (see below)
- Navigate through the GraphiQL Documentation Explorer.
- Change the [settings](settings.md).
- Explore the [api](api.md).
- [Override email templates](overriding-email-templates.md).
- Explore [these useful links](community.md).

### Full schema

```python tab="GraphQL"
class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
```

```python tab="Relay"
class AuthMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    resend_activation_email = relay.ResendActivationEmail.Field()
    send_password_reset_email = relay.SendPasswordResetEmail.Field()
    password_reset = relay.PasswordReset.Field()
    password_change = relay.PasswordChange.Field()
    archive_account = relay.ArchiveAccount.Field()
    delete_account = relay.DeleteAccount.Field()
    update_account = relay.UpdateAccount.Field()
    send_secondary_email_activation = relay.SendSecondaryEmailActivation.Field()
    verify_secondary_email = relay.VerifySecondaryEmail.Field()
    swap_emails = relay.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()
```

### Full Allow Any Classes

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
