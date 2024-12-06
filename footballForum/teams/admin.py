from django.contrib import admin
from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'stadium', 'foundation_year',)

    search_fields = ('name',)

    ordering = ('pk',)

    fieldsets = (
        ('Team info', {'fields': ('name', 'foundation_year')}),
        ('Other info', {'fields': ('logo', 'stadium')}),
    )
