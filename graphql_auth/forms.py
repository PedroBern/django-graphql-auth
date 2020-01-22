from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


from .utils import flat_dict
from .settings import graphql_auth_settings


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = flat_dict(
            graphql_auth_settings.REGISTER_MUTATION_FIELDS
        ) + flat_dict(graphql_auth_settings.REGISTER_MUTATION_FIELDS_OPTIONAL)


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=254,)
