# quickauth/apps.py
from django.apps import AppConfig

class SomeAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'someauth'

    def ready(self):
        # import signals here to avoid early execution
        from . import signals  # noqa
