from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings as django_settings

from .models import UserStatus


@receiver(post_save, sender=django_settings.AUTH_USER_MODEL)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserStatus._default_manager.get_or_create(user=instance)
