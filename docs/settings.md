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

## Dynamic Fields

Fields that you can choose.

### Basics

All fields should match name in the user model field.

\* Can be a list of string fields or a dictionary mapping fields and [graphene base scalars](https://docs.graphene-python.org/en/latest/types/scalars/#base-scalars).

Example:

```python

update_fields_list = ["username", "first_name", "last_name"]

# same as:

update_fields_dict = {
    "username": "String",
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

default: `#!python ["email", "username"]` [\*](/settings/#basics)

### REGISTER_MUTATION_FIELDS_OPTIONAL

Optional fields on registration.

default: `#!python []` [\*](/settings/#basics)

### UPDATE_MUTATION_FIELDS

Optional fields on update account.

default: `#!python ["username", "first_name", "last_name"]` [\*](/settings/#basics)

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

---

## Logout options

These settings will work only if using [long running refresh tokens](https://django-graphql-jwt.domake.io/en/latest/refresh_token.html#long-running-refresh-tokens). It allow to revoke all user tokens in the database.

### LOGOUT_ON_PASSWORD_RESET

default: `#!python True`

### LOGOUT_ON_PASSWORD_CHANGE

default: `#!python True`

---

## Email

### SEND_ACTIVATION_EMAIL

If set to `#!python False`, user will be saved with `#!python is_active=True` on the database.

If `#!python True`, is saved with `#!python is_active=False` and need to to activate account via email.

default: `#!python True`

### EMAIL_FROM

It will get the default value from your settings, but you can provide a specific email.

default: `#!python getattr(django_settings, "DEFAULT_FROM_EMAIL", "test@email.com")`

### ACTIVATION_PATH_ON_EMAIL

Path [variable](/overriding-email-templates/#email-variables) used in activation email.

default: `#!python "activate"`

### PASSWORD_RESET_PATH_ON_EMAIL

Path [variable](/overriding-email-templates/#email-variables) used in password reset email.

default: `#!python "password-reset"`

---

## Email templates

You can override email templates as shown [here](/overriding-email-templates), but you can also change the templates names.

### EMAIL_SUBJECT_ACTIVATION

default: `#!python "email/activation_subject.txt"`

### EMAIL_SUBJECT_RESEND_ACTIVATION

default: `#!python "email/activation_subject.txt"`

### EMAIL_SUBJECT_PASSWORD_RESET

default: `#!python "email/password_reset_subject.txt"`

### EMAIL_TEMPLATE_ACTIVATION

default: `#!python "email/activation_email.html"`

### EMAIL_TEMPLATE_RESEND_ACTIVATION

default: `#!python "email/activation_email.html"`

### EMAIL_TEMPLATE_PASSWORD_RESET

default: `#!python "email/password_reset_email.html"`
