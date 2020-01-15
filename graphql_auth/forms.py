from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
    SetPasswordForm as DjangoSetPasswordForm,
)
from django.contrib.auth import get_user_model
from django import forms


from .settings import settings

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = settings.MUTATION_FIELDS_REGISTER


class PasswordChangeForm(DjangoPasswordChangeForm):
    """Password change form"""


class SetPasswordForm(DjangoSetPasswordForm):
    """Password change form without old password"""


class UpdateAccountForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = settings.MUTATION_FIELDS_UPDATE.keys()


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=254,)
