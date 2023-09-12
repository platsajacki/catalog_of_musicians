from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser

from .permissions import IsSafeMethod


class LookUpSlugFieldMixin:
    """
    Добавляет поле 'lookup_field' со значением 'slug'
    для создания url-путей с использованием 'slug' вместо 'id'.
    """
    class Meta:
        abstract = True
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class PermissionFilterSearchMixin:
    """Добавляет общие настройки для view."""
    permission_classes = [IsSafeMethod | IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['name']
