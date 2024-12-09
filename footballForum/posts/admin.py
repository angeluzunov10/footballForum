from django.contrib import admin

from footballForum.posts.models import Post


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'created_at',
        'updated_at',
        'approved',
    )

    search_fields = ('author__username', 'author__email', 'title')

    ordering = ('pk',)

    fieldsets = (
        ('Post info', {'fields': ('author', 'title', 'approved')}),
        ('Tags', {'fields': ('tagged_teams', 'tagged_players',)}),
        ('Content', {'fields': ('image', 'content',)}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    readonly_fields = ('author', 'title', 'image', 'content', 'created_at', 'updated_at',)
