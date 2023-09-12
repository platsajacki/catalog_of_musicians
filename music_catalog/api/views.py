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
from constants import MUSICIAN_SCHEMA, SONG_SCHEMA, ALBUM_SCHEMA
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


@extend_schema_view(**MUSICIAN_SCHEMA)
class MusicianViewSet(PermissionFilterSearchMixin, viewsets.ModelViewSet):
    """Представление для управления информацией об исполнителях музыки."""
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'musician'


@extend_schema_view(**SONG_SCHEMA)
class SongViewSet(PermissionFilterSearchMixin, viewsets.ModelViewSet):
    """Представление для управления информацией о музыкальных произведениях."""
    serializer_class = SongSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'song'

    def get_queryset(self) -> Song:
        """Оптимизирует запрос музыкальных произведений."""
        return Song.objects.filter(albums=self.get_album())

    def get_album(self) -> Album:
        """Получает объект альбома по параметрам URL."""
        return get_object_or_404(Album, slug=self.kwargs['album'])


@extend_schema_view(**ALBUM_SCHEMA)
class AlbumViewSet(PermissionFilterSearchMixin, viewsets.ModelViewSet):
    """Представление для управления информацией об альбомах."""
    serializer_class = AlbumSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'album'

    def get_musician(self) -> Musician:
        """Получает объект музыканта по параметрам URL."""
        return get_object_or_404(Musician, slug=self.kwargs['musician'])

    def get_queryset(self) -> Album:
        """Оптимизирует запрос запрос альбомов."""
        return Album.objects.filter(musician=self.get_musician())

    def perform_create(self, serializer: AlbumSerialiser) -> None:
        """Создает новый альбом и связывает его с музыкантом."""
        serializer.save(musician=self.get_musician())
