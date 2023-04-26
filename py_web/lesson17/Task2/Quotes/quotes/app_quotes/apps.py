from django.apps import AppConfig


class AppQuotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_quotes'

    def ready(self):
        import app_quotes.signals  # noqa
