from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"  # e.g: "username", "email"
    EMAIL_FIELD = "email"  # e.g: "email", "primary_email"
