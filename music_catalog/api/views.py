from typing import Any

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from .permissions import IsSafeMethod
from .serializers import MusicianSerializer
from music.models import Musician


class MusicianViewSet(viewsets.ModelViewSet):
    """
    Представление для управления информацией об исполнителях музыки.
    """
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    lookup_field = 'slug'
    permission_classes = [IsSafeMethod | IsAdminUser]

    def list(
            self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """
        Получить информацию об исполнителях музыки.
        Доступно всем пользователям.
        """
        return super().list(request, *args, **kwargs)

    def create(
            self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """
        Обновить информацию о исполнителе музыки.
        Доступно только администратору.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(
            self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """
        Получить информацию о конкретном исполнителе музыки.
        Доступно всем пользователям.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Обновить информацию о конкретном исполнителе музыки.
        Доступно только администратору.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновить информацию о конкретном исполнителе музыки.
        Доступно только администратору.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удалить информацию о конкретном исполнителе музыки.
        Доступно только администратору.
        """
        return super().destroy(request, *args, **kwargs)
