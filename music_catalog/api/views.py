from typing import Any

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .mixins import PermissionFilterSearchMixin
from .serializers import (
    AdminLoginSerializer, MusicianSerializer, SongSerialiser, AlbumSerialiser
)
from music.models import User, Musician, Song, Album


class AdminLoginView(generics.CreateAPIView):
    """Представление для выполнения входа администратора."""
    serializer_class = AdminLoginSerializer

    @extend_schema(
        summary='Вход в систему.',
        responses={
            status.HTTP_200_OK: TokenRefreshSerializer
        }
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Выполняет аутентификацию администратора,
        возвращает токены доступа и обновления в ответе.
        """
        serializer: dict[str, str] = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.context['user']
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token)})


@extend_schema_view(
    list=extend_schema(
        summary='Получить всех исполнителей.',
        description=(
            'Получить информацию об исполнителях музыки. '
            'Доступно всем пользователям.'
        ),
    ),
    create=extend_schema(
        summary='Создать исполнителя.',
        description=(
            'Создать информацию о исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
    retrieve=extend_schema(
        summary='Получить исполнителя.',
        description=(
            'Получить информацию о конкретном исполнителе музыки. '
            'Доступно всем пользователям.'
        ),
    ),
    update=extend_schema(
        summary='Обновить информацию исполнителя.',
        description=(
            'Обновить информацию о конкретном исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
    partial_update=extend_schema(
        summary='Частично обновить информацию исполнителя.',
        description=(
            'Частично обновить информацию о конкретном исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
    destroy=extend_schema(
        summary='Удалить информацию об исполнителе.',
        description=(
            'Удалить информацию о конкретном исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
)
class MusicianViewSet(PermissionFilterSearchMixin, viewsets.ModelViewSet):
    """Представление для управления информацией об исполнителях музыки."""
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'musician'


class SongViewSet(PermissionFilterSearchMixin, viewsets.ModelViewSet):
    """Представление для управления информацией о музыкальных произведениях."""
    queryset = Song.objects.all()
    serializer_class = SongSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'song'


class AlbumViewSet(PermissionFilterSearchMixin, viewsets.ModelViewSet):
    """Представление для управления информацией об альбомах."""
    queryset = Album.objects.all()
    serializer_class = AlbumSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'album'

    def get_musician(self) -> Musician:
        return get_object_or_404(Musician, slug=self.kwargs['musician'])

    def perform_create(self, serializer: AlbumSerialiser):
        serializer.save(musician=self.get_musician())
