from django.contrib.auth import get_user_model
from django.db import models

from footballForum.players.models import Player
from footballForum.teams.models import Team

UserModel = get_user_model()


class Post(models.Model):
    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    author = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    image = models.URLField()

    tagged_players = models.ManyToManyField(
        to=Player,
        blank=True,
        related_name='tagged_posts'
    )

    tagged_teams = models.ManyToManyField(
        to=Team,
        blank=True,
        related_name='tagged_posts'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    approved = models.BooleanField(
        default=False
    )

    class Meta:
        permissions = [
            ('approve_post', 'Can approve posts'),
        ]

    def __str__(self):
        return self.title
