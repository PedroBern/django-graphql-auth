Django GraphQL Auth
===================

|Pypi| |Build Status| |Codecov|

GraphQL authentication for `Django <https://github.com/django/django>`_!

Features
--------

* Fully compatible with `Relay <https://github.com/facebook/relay>`_
* Works with default/custom user model
* JWT authentication (with `Django GraphQL JWT <https://github.com/flavors/django-graphql-jwt>`_)
* User query with filters (with `Django Filter <https://github.com/carltongibson/django-filter>`_ and `Graphene Django <https://github.com/graphql-python/graphene-django>`_)
* User registration with email verification
* Resend activation email
* Retrieve/Update user
* Archive user
* Permanently delete user
* Turn archived user active again on login
* Password change
* Password reset through email
* Revoke user tokens on account archive and password change/reset
* All mutations return ``success`` and ``errors``
* Customizable

.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-auth.svg
   :target: https://pypi.org/project/django-graphql-auth/
   :alt: Pypi

.. |Build Status| image:: https://travis-ci.com/pedrobern/django-graphql-auth.svg?branch=master
   :target: https://travis-ci.com/pedrobern/django-graphql-auth
   :alt: Build Status

.. |Codecov| image:: https://img.shields.io/codecov/c/github/pedrobern/django-graphql-auth/master.svg?style=flat-square
   :target: https://codecov.io/gh/pedrobern/django-graphql-auth/
   :alt: Codecov
