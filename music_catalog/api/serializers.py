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

    def validate_number_in_album(self, value: int) -> int:
        """Проверяет уникальность порядкового номера песни в альбоме."""
        album_song: AlbumSong | None = AlbumSong.objects.filter(
            album=self.context['view'].get_album(), number_in_album=value
        ).first()
        if (
            album_song and album_song.number_in_album != value
            or album_song and self.context['request'].method == 'POST'
        ):
            raise serializers.ValidationError(
                'В альбоме уже есть песня с таким порядковым номером.'
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> Song:
        """Создает новую песню и связывает ее с альбомом."""
        album: Album = self.context['view'].get_album()
        number_in_album: int = validated_data['number_in_album']
        if AlbumSong.objects.filter(
            album=album, number_in_album=number_in_album
        ).exists():
            raise serializers.ValidationError(
                'В альбоме уже есть песня с таким порядковым номером.'
            )
        song: Song = Song.objects.create(
            name=validated_data['name'],
            slug=validated_data['slug']
        )
        AlbumSong.objects.create(
            album=album, song=song,
            number_in_album=number_in_album
        )
        return song

    def update(self, instance: Song, validated_data: dict[str, Any]) -> Song:
        """Обновляет данные песни и связанной с ней информации в альбоме."""
        album_song: AlbumSong = AlbumSong.objects.get(
            song=instance, album=self.context['view'].get_album()
        )
        album_song.number_in_album = validated_data['number_in_album']
        album_song.save()
        return super().update(instance, validated_data)

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
