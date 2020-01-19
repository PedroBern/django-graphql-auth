# Django GraphQL Auth

[![Codecov Coverage](https://img.shields.io/codecov/c/github/pedrobern/django-graphql-auth/master.svg?style=flat-square)](https://codecov.io/gh/pedrobern/django-graphql-auth/)
[![Build Status](https://travis-ci.com/pedrobern/django-graphql-auth.svg?branch=master)](https://travis-ci.com/pedrobern/django-graphql-auth)
[![Pypi](https://img.shields.io/pypi/v/django-graphql-auth.svg)](https://pypi.org/project/django-graphql-auth/)

---

GraphQL implementation of the [Django](https://github.com/django/django)
authentication system.

It abstract all the basic logic of handling user accounts out of your app,
so you don't need to think about it and can **get up and running faster**.

No lock-in. When you are ready to implement your own code or this package
is not up to your expectations , it's *easy to extend or switch to
your implementation*.

---

## Features

* [x] Awesome docs :tada:
* [x] Fully compatible with [Relay](https://github.com/facebook/relay>)
* [x] Works with default/custom user model
* [x] JWT authentication <small>(with [Django GraphQL JWT](https://github.com/flavors/django-graphql-jwt>))</small>
* [x] User query with filters <small>(with [Django Filter](https://github.com/carltongibson/django-filter>) and [Graphene Django](https://github.com/graphql-python/graphene-django>))</small>
* [x] User registration with email verification
* [x] Resend activation email
* [x] Retrieve/Update user
* [x] Archive user
* [x] Permanently delete user
* [x] Turn archived user active again on login
* [x] Password change
* [x] Password reset through email
* [x] Revoke user tokens on account archive and password change/reset
* [x] All mutations return `success` and `errors`
* [x] Default email templates (you will customize though)
* [x] Customizable, no lock-in

---

## Documentation

Documentation is available at \# TODO
