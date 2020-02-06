from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    this model is used to test:
        - non_field_errors on form (see update account test b)
    """

    pass

    class Meta:
        unique_together = ("first_name", "last_name")
