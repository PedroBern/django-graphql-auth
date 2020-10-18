from django.db.models.signals import post_save
from django.conf import settings as django_settings

from django.dispatch import Signal, receiver


@receiver(post_save, sender=django_settings.AUTH_USER_MODEL)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        from .models import UserStatus

        UserStatus._default_manager.get_or_create(user=instance)


user_registered = Signal()
user_verified = Signal()
