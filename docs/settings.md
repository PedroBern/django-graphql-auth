# Settings

---

## Example

Configuration is made from a single Django setting named `#!python GRAPHQL_AUTH`.

```python
# settings.py

GRAPHQL_AUTH = {
    'LOGIN_ALLOWED_FIELDS': ['email', 'username'],
    # ...
}
```

---

## Boolean Flags


### ALLOW_LOGIN_NOT_VERIFIED

Determines whether the user can log in without being verified. If it is true, the registring returns `token` and `refresh token` on the output.

default: `#!python True`

### ALLOW_LOGIN_WITH_SECONDARY_EMAIL

If a user has a secondary email set, he can use to login.

default: `#!python True`

### ALLOW_PASSWORDLESS_REGISTRATION

To allow registration with no password; Django `set_unusable_password()` will be used in setting the default password.

- User cannot login until they set their password

default: `#!python False`

### ALLOW_DELETE_ACCOUNT

Instead of deleting the account, make `#!python user.is_active=False`.

If set to `#!python True`, will actually delete the account.

default: `#!python False`

### SEND_ACTIVATION_EMAIL

If set to `#!python False`, no email will be sent.

Note that users will still have an `#!python verified=False` status.

default: `#!python True`

### SEND_PASSWORD_SET_EMAIL

If set to `#!python True`, user will be notified to set their password after registration - dependent on `ALLOW_PASSWORDLESS_REGISTRATION`.

default: `#!python False`

---

## Dynamic Fields

Fields that you can choose.

### Basics

All fields should match name in the user model field.

\* Can be a list of string fields or a dictionary mapping fields and [graphene base scalars](https://docs.graphene-python.org/en/latest/types/scalars/#base-scalars).

Example:

```python

update_fields_list = ["first_name", "last_name"]

# same as:

update_fields_dict = {
    "first_name": "String",
    "last_name": "String",
}

# maybe you have some Int that you want on registration:

REGISTER_MUTATION_FIELDS = {
    "email": "String",
    "username": "String",
    "luck_number": "Int",
}
```

### LOGIN_ALLOWED_FIELDS

default: `#!python ["email", "username"]`

### REGISTER_MUTATION_FIELDS

Required fields on registration, along with `password1` and `password2`.

default: `#!python ["email", "username"]`

### REGISTER_MUTATION_FIELDS_OPTIONAL

Optional fields on registration.

default: `#!python []`

### UPDATE_MUTATION_FIELDS

Optional fields on update account.

default: `#!python ["first_name", "last_name"]`

### CUSTOM_ERROR_TYPE

Customize mutations error output by providing a Graphene type.

default: `graphql_auth.types.ExpectedErrorType`

example:
```python
class CustomErrorType(graphene.Scalar):
    @staticmethod
    def serialize(errors):
        return {"my_custom_error_format"}
```

---

## Query

### USER_NODE_FILTER_FIELDS

Learn more on [graphene django](https://docs.graphene-python.org/projects/django/en/latest/filtering/) and [django filter](https://django-filter.readthedocs.io/en/master/guide/usage.html#the-filter).

default:
```python
{
    "email": ["exact",],
    "username": ["exact", "icontains", "istartswith"],
    "is_active": ["exact"],
    "status__archived": ["exact"],
    "status__verified": ["exact"],
    "status__secondary_email": ["exact"],
}
```

### USER_NODE_EXCLUDE_FIELDS

default: `#!python ["password", "is_superuser"]`

---

## Token expirations

### EXPIRATION_ACTIVATION_TOKEN

default: `#!python timedelta(days=7)`

### EXPIRATION_PASSWORD_RESET_TOKEN

default: `#!python timedelta(hours=1)`

### EXPIRATION_SECONDARY_EMAIL_ACTIVATION_TOKEN

default: `#!python timedelta(hours=1)`

### EXPIRATION_PASSWORD_SET_TOKEN

default: `#!python timedelta(days=7)`

---

## Email

### EMAIL_FROM

It will get the default value from your settings, but you can provide a specific email.

default: `#!python getattr(django_settings, "DEFAULT_FROM_EMAIL", "test@email.com")`

### ACTIVATION_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md) used in activation email.

default: `#!python "activate"`

### PASSWORD_RESET_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md) used in password reset email.

default: `#!python "password-reset"`

### PASSWORD_SET_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md) used in password set email.

default: `#!python "password-set"`

### ACTIVATION_SECONDARY_EMAIL_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md) used in secondary email activation email.

default: `#!python "activate"`

### EMAIL_ASYNC_TASK

String path to wrapper function of all email sending functions. This function must have accepts 2 arguments: the send email function and a tuple of arguments.

Notice that this is pseudo async support, just a hook to let you implement the async code.

Basic usage with celery:

```python
from celery import task

@task
def graphql_auth_async_email(func, args):
    """
    Task to send an e-mail for the graphql_auth package
    """
    return func(*args)
```

For the example above, the setting would be:

```python
GRAPHQL_AUTH = {
    "EMAIL_ASYNC_TASK": "path/to/file.graphql_auth_async_email"
}
```

default: `#!python False`

---

## Email subject templates

You can override email templates as shown [here](overriding-email-templates.md), but you can also change the templates names.

### EMAIL_SUBJECT_ACTIVATION

default: `#!python "email/activation_subject.txt"`

### EMAIL_SUBJECT_ACTIVATION_RESEND

default: `#!python "email/activation_subject.txt"`

### EMAIL_SUBJECT_SECONDARY_EMAIL_ACTIVATION

default: `#!python "email/activation_subject.txt"`

### EMAIL_SUBJECT_PASSWORD_RESET

default: `#!python "email/password_reset_subject.txt"`

### EMAIL_SUBJECT_PASSWORD_SET

default: `#!python "email/password_set_subject.txt"`


---

## Email templates

You can override email templates as shown [here](overriding-email-templates.md), but you can also change the templates names.


### EMAIL_TEMPLATE_ACTIVATION

default: `#!python "email/activation_email.html"`

### EMAIL_TEMPLATE_ACTIVATION_RESEND

default: `#!python "email/activation_email.html"`

### EMAIL_TEMPLATE_SECONDARY_EMAIL_ACTIVATION

default: `#!python "email/activation_email.html"`

### EMAIL_TEMPLATE_PASSWORD_RESET

default: `#!python "email/password_reset_email.html"`

### EMAIL_TEMPLATE_PASSWORD_SET

default: `#!python "email/password_set_email.html"`

### EMAIL_TEMPLATE_VARIABLES

default: `#!python {}`

Dictionary of key value pairs of template variables that will be injected into the templates.

Example:

```python
GRAPHQL_AUTH = {
    "EMAIL_TEMPLATE_VARIABLES": {
        "frontend_domain": "the-frontend.com"
    }
}
```

Now, in the templates:
{% raw %}

```html
<p>{{ protocol }}://{{ frontend_domain }}/{{ path }}/{{ token }}</p>
```

{% endraw %}
