from django.db import models


class Team(models.Model):
    name = models.CharField(
        max_length=100,
    )

    logo = models.URLField()

    stadium = models.CharField(
        max_length=100
    )

    foundation_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
