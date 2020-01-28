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


Documentation
-------------

Documentation is available at `read the docs <https://django-graphql-auth.readthedocs.io/en/latest/>`_.

Features
--------

* `Awesome docs <https://django-graphql-auth.readthedocs.io/en/latest/>`_
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


Preview
-------

Handling user accounts becomes super easy.

.. code:: bash

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

Check the status of the new user:

.. code:: python

  u = UserModel.objects.last()
  u.status.verified
  # False


During the registration, an email with a verification link was sent.

.. code:: bash

  mutation {
    verifyAccount(
      token:"<TOKEN ON EMAIL LINK>",
    ) {
      success,
      errors
    }
  }

Now user is verified.

.. code:: python

  u.status.verified
  # True


Check the `installation guide <https://django-graphql-auth.readthedocs.io/en/latest/installation/>`_ or jump to the `quickstart <https://django-graphql-auth.readthedocs.io/en/latest/quickstart/>`_. Or if you prefer, browse the `api <https://django-graphql-auth.readthedocs.io/en/latest/api/>`_.

.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-auth.svg
   :target: https://pypi.org/project/django-graphql-auth/
   :alt: Pypi

.. |Build Status| image:: https://travis-ci.com/pedrobern/django-graphql-auth.svg?branch=master
   :target: https://travis-ci.com/pedrobern/django-graphql-auth
   :alt: Build Status

.. |Codecov| image:: https://img.shields.io/codecov/c/github/pedrobern/django-graphql-auth/master.svg?style=flat-square
   :target: https://codecov.io/gh/pedrobern/django-graphql-auth/
   :alt: Codecov
