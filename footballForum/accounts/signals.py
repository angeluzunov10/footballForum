from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models.app_profile import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):   # signal for creating a profile after creating a user
    if created:
        Profile.objects.create(
            user=instance,
        )
