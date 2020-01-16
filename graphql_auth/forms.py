from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
    SetPasswordForm as DjangoSetPasswordForm,
)
from django.contrib.auth import get_user_model
from django import forms

from .utils import set_fields
from .settings import graphql_auth_settings as settings


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = set_fields(settings.REGISTER_MUTATION_FIELDS) + set_fields(
            settings.REGISTER_MUTATION_FIELDS_OPTIONAL
        )


class PasswordChangeForm(DjangoPasswordChangeForm):
    """Password change form"""


class SetPasswordForm(DjangoSetPasswordForm):
    """Password change form without old password"""


class UpdateAccountForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = set_fields(settings.UPDATE_MUTATION_FIELDS)


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=254,)
