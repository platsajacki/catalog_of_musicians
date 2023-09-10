from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .superuser import create_admin_user


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'

    def ready(self) -> None:
        post_migrate.connect(create_admin_user, sender=self)
