# Django GraphQL Auth

[Django](https://github.com/django/django) registration and authentication with GraphQL.

[![downloads](https://img.shields.io/pypi/dm/django-graphql-auth)](https://pypistats.org/packages/django-graphql-auth)
[![Codecov Coverage](https://img.shields.io/codecov/c/github/pedrobern/django-graphql-auth/master.svg?style=flat-square)](https://codecov.io/gh/pedrobern/django-graphql-auth/)
[![Build Status](https://travis-ci.com/pedrobern/django-graphql-auth.svg?branch=master)](https://travis-ci.com/pedrobern/django-graphql-auth)
[![Pypi](https://img.shields.io/pypi/v/django-graphql-auth.svg)](https://pypi.org/project/django-graphql-auth/)
[![Documentation Status](https://readthedocs.org/projects/django-graphql-auth/badge/?version=latest)](https://django-graphql-auth.readthedocs.io/en/latest/?badge=latest)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/pedrobern/django-graphql-auth/blob/master/CONTRIBUTING.md)

## Demo

![Demo Video](https://github.com/pedrobern/django-graphql-auth/blob/master/demo.gif)

## About

Abstract all the basic logic of handling user accounts out of your app,
so you don't need to think about it and can **get up and running faster**.

No lock-in. When you are ready to implement your own code or this package
is not up to your expectations , it's *easy to extend or switch to
your implementation*.


## Documentation

Documentation is available at [read the docs](https://django-graphql-auth.readthedocs.io/en/latest/).


## Features

* [x] [Awesome docs](https://django-graphql-auth.readthedocs.io/en/latest/) :tada:
* [x] Fully compatible with [Relay](https://github.com/facebook/relay>)
* [x] Works with **default or custom** user model
* [x] JWT authentication *(with [Django GraphQL JWT](https://github.com/flavors/django-graphql-jwt))*
* [x] User query with filters *(with [Django Filter](https://github.com/carltongibson/django-filter) and [Graphene Django](https://github.com/graphql-python/graphene-django))*
* [x] User registration with email verification
* [x] Add secondary email, with email verification too
* [x] Resend activation email
* [x] Retrieve/Update user
* [x] Archive user
* [x] Permanently delete user or make it inactive
* [x] Turn archived user active again on login
* [x] Track user status (archived, verified, secondary email)
* [x] Password change
* [x] Password reset through email
* [x] Revoke user refresh tokens on account archive/delete/password change/reset
* [x] All mutations return `success` and `errors`
* [x] Default email templates *(you will customize though)*
* [x] Customizable, no lock-in

## Full Schema

```python

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


## Relay

Import mutations from the ``relay`` module:

```python

from graphql_auth import relay

class AuthMutation(graphene.ObjectType):
   register = relay.Register.Field()
   # ...
```


## Example

Handling user accounts becomes super easy.

```python
mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password1: "123456super",
    password2: "123456super",
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

Check the status of the new user:

```python
u = UserModel.objects.last()
u.status.verified
# False
```

During the registration, an email with a verification link was sent.

```python
mutation {
  verifyAccount(
    token:"<TOKEN ON EMAIL LINK>",
  ) {
    success,
    errors
  }
}
```

Now user is verified.

```python
u.status.verified
# True
```

Check the [installation guide](https://django-graphql-auth.readthedocs.io/en/latest/installation/) or jump to the [quickstart](https://django-graphql-auth.readthedocs.io/en/latest/quickstart/). Or if you prefer, browse the [api](https://django-graphql-auth.readthedocs.io/en/latest/api/).


## Contributing

See [CONTRIBUTING.md](https://github.com/pedrobern/django-graphql-auth/blob/master/CONTRIBUTING.md)
