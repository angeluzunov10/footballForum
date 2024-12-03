from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from ..managers import AppUserManager


class AppUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    username = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return self.username or self.email
