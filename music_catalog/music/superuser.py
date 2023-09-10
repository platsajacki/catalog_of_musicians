from os import getenv
from typing import Any

from django.contrib.auth import get_user_model


def create_admin_user(**kwargs: dict[str, Any]) -> None:
    """Функция для создания администратора, если он не существует."""
    User = get_user_model()
    if not User.objects.filter(username=getenv('ADMIN_LOGIN')).exists():
        User.objects.create_superuser(
            username=getenv('ADMIN_LOGIN'),
            password=getenv('ADMIN_PASSWORD')
        )
