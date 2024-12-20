from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'footballForum.accounts'

    def ready(self):
        import footballForum.accounts.signals
