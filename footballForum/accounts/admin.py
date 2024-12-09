from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from footballForum.accounts.forms import AppUserRegisterForm, AppUserChangeForm
from footballForum.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    model = UserModel

    add_form = AppUserRegisterForm

    form = AppUserChangeForm

    list_display = (
        'pk',
        'email',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
        'loyal_user'
    )

    search_fields = ('email',)

    ordering = ('pk',)

    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'login_count', 'loyal_user')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('login_count', 'loyal_user',)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'location')

    search_fields = ('last_name',)

    ordering = ('pk',)

    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth',)}),
        ('Other info', {'fields': ('location', 'profile_picture')})
    )
