from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.contrib.auth import get_user_model
from django import forms

from .utils import flat_dict
from .settings import graphql_auth_settings as app_settings


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = flat_dict(app_settings.REGISTER_MUTATION_FIELDS) + flat_dict(
            app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL
        )


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=254)


class CustomUsernameField(UsernameField):
    required = False


class UpdateAccountForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = flat_dict(app_settings.UPDATE_MUTATION_FIELDS)
        field_classes = {"username": CustomUsernameField}


class PasswordLessRegisterForm(UserCreationForm):
    """
    A RegisterForm with optional password inputs.
    """

    class Meta:
        model = get_user_model()
        fields = flat_dict(app_settings.REGISTER_MUTATION_FIELDS) + flat_dict(
            app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL
        )

    def __init__(self, *args, **kwargs):
        super(PasswordLessRegisterForm, self).__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
