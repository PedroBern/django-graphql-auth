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

### ALLOW_DELETE_ACCOUNT

Instead of deleting the account, make `#!python user.is_active=False`.

If set to `#!python True`, will actually delete the account.

default: `#!python False`

### SEND_ACTIVATION_EMAIL

If set to `#!python False`, no email will be sent.

Note that users will still have an `#!python verified=False` status.

default: `#!python True`

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

default: `#!python ["email", "username"]` [\*](settings.md/#basics)

### REGISTER_MUTATION_FIELDS_OPTIONAL

Optional fields on registration.

default: `#!python []` [\*](settings.md/#basics)

### UPDATE_MUTATION_FIELDS

Optional fields on update account.

default: `#!python ["first_name", "last_name"]` [\*](settings.md/#basics)

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

---

## Email

### EMAIL_FROM

It will get the default value from your settings, but you can provide a specific email.

default: `#!python getattr(django_settings, "DEFAULT_FROM_EMAIL", "test@email.com")`

### ACTIVATION_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md/#email-variables) used in activation email.

default: `#!python "activate"`

### PASSWORD_RESET_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md/#email-variables) used in password reset email.

default: `#!python "password-reset"`

### ACTIVATION_SECONDARY_EMAIL_PATH_ON_EMAIL

Path [variable](overriding-email-templates.md/#email-variables) used in secondary email activation email.

default: `#!python "activate"`

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
