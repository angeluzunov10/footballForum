from django.contrib import admin
from footballForum.players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'team', 'position')

    search_fields = ('name', 'team__name', 'position')

    ordering = ('pk',)

    fieldsets = (
        ('Personal info', {'fields': ('name', 'player_picture')}),
        ('Club info', {'fields': ('team', 'position')}),
    )