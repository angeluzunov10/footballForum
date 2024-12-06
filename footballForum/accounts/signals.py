from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model, user_logged_in
from .models.app_profile import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):   # signal for creating a profile after creating a user
    if created:
        Profile.objects.create(
            user=instance,
        )


@receiver(user_logged_in)
def increment_login_count(sender, request, user, **kwargs):
    if isinstance(user, UserModel):
        user.login_count += 1
        user.save()
