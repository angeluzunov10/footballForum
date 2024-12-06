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

    login_count = models.PositiveIntegerField(default=0)
    loyal_user = models.BooleanField(
        default=False,
        editable=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.loyal_user = True
        else:
            if self.login_count >= 10:
                self.loyal_user = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username or self.email
