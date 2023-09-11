from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .mixins import LookUpSlugFieldMixin
from music.models import User, Musician, Song, Album, AlbumSong


class AdminLoginSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации администраторов."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator()
        ]
    )

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Проверяет введенные учетные данные и статус администратора."""
        username: str = attrs.get('username')
        password: str = attrs.get('password')
        user: User | None = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Неправильный логин или пароль.')
        if not user.is_staff:
            raise serializers.ValidationError(
                'Доступ запрещен. Вы не являетесь администратором.'
            )
        self.context['user'] = user
        return super().validate(attrs)

    class Meta:
        model = User
        fields = ('username', 'password')


class MusicianSerializer(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """
    Сериализатор для информации об исполнителях.
    Поддерживает создание и обновление данных об исполнителях.
    """
    class Meta:
        model = Musician
        fields = ('name', 'slug')


class SongSerialiser(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """
    Сериализатор для информации о музыкальных произведениях.
    Поддерживает создание и обновление данных музыкальных произведений.
    """
    number_in_album = serializers.IntegerField(required=True)

    class Meta:
        model = Song
        fields = ('name', 'slug', 'number_in_album')

    def create(self, validated_data: dict[str, str]) -> Song:
        """Создает новую песню и связывает ее с альбомом."""
        song: Song = Song.objects.create(
            name=validated_data['name'],
            slug=validated_data['slug']
        )
        album: Album = self.context['view'].get_album()
        AlbumSong.objects.create(
            album=album, song=song,
            number_in_album=validated_data['number_in_album']
        )
        return song

    def to_representation(self, instance: Song) -> dict[str, Any]:
        """Готовит данные для ответа клиенту."""
        number_in_album: int = AlbumSong.objects.get(
            song=instance,
            album=self.context['view'].get_album()
        ).number_in_album
        return {
            'name': instance.name,
            'slug': instance.slug,
            'number_in_album': number_in_album
        }


class AlbumSerialiser(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """
    Сериализатор для информации о альбомах.
    Поддерживает создание и обновление данных альбомов.
    """
    musician = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True
    )
    total_songs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'musician',
            'total_songs', 'year_of_release'
        )

    def get_total_songs(self, obj: Album) -> int:
        """Метод для вычисления общего количества песен в альбоме."""
        return obj.songs.count()
