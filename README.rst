Django GraphQL Auth
===================

|Pypi| |Build Status| |Codecov|


GraphQL implementation of the `Django <https://github.com/django/django>`_
authentication system.

It abstract all the basic logic of handling user accounts out of your app,
so you don't need to think about it and can **get up and running faster**.

No lock-in. When you are ready to implement your own code or this package
is not up to your expectations , it's easy to extend or switch to
your implementation.


Features
--------

* Awesome docs
* Fully compatible with `Relay <https://github.com/facebook/relay>`_
* Works with default/custom user model
* JWT authentication (with `Django GraphQL JWT <https://github.com/flavors/django-graphql-jwt>`_)
* User query with filters (with `Django Filter <https://github.com/carltongibson/django-filter>`_ and `Graphene Django <https://github.com/graphql-python/graphene-django>`_)
* User registration with email verification
* Resend activation email
* Add secondary email, with email verification too
* Retrieve/Update user
* Archive user
* Permanently delete user or make it inactive
* Turn archived user active again on login
* Track user status (archived, verified, secondary email)
* Password change
* Password reset through email
* Revoke user refresh tokens on account archive/delete/password change/reset
* All mutations return ``success`` and ``errors``
* Default email templates *(you will customize though)*
* Customizable, no lock-in

Documentation
-------------

Documentation is available at # TODO


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-auth.svg
   :target: https://pypi.org/project/django-graphql-auth/
   :alt: Pypi

.. |Build Status| image:: https://travis-ci.com/pedrobern/django-graphql-auth.svg?branch=master
   :target: https://travis-ci.com/pedrobern/django-graphql-auth
   :alt: Build Status

.. |Codecov| image:: https://img.shields.io/codecov/c/github/pedrobern/django-graphql-auth/master.svg?style=flat-square
   :target: https://codecov.io/gh/pedrobern/django-graphql-auth/
   :alt: Codecov
