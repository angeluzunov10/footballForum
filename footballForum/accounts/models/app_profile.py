from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )

    first_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    profile_picture = models.URLField(
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    favorite_team = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
