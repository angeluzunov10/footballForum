from django.db import models
from footballForum.teams.models import Team


class PositionChoices(models.TextChoices):
    GOALKEEPER = 'GK', 'Goalkeeper'
    DEFENDER = 'DEF', 'Defender'
    MIDFIELDER = 'MID', 'Midfielder'
    STRIKER = 'ST', 'Striker'


class Player(models.Model):
    name = models.CharField(
        max_length=100
    )

    position = models.CharField(
        max_length=50,
        choices=PositionChoices.choices,
    )

    team = models.ForeignKey(
        to=Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='players',
    )

    player_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
