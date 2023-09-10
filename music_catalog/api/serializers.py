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
    # number_in_album = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('name', 'slug',  # 'number_in_album'
                  )

    # def get_number_in_album(self, obj: Song) -> int:
    #     """Получает объект AlbumSong, связанный с текущей песней (obj)."""
    #     album = Album.objects.get(slug=self.context['album'])
    #     album_song, _ = AlbumSong.objects.get_or_create(
    #         album=album,
    #         song=obj
    #     )
    #     return album_song.number_in_album


class AlbumSerialiser(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """
    Сериализатор для информации о альбомах.
    Поддерживает создание и обновление данных альбомов.
    """
    musician = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True
    )
    songs = SongSerialiser(many=True, read_only=True)

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'musician',
            'songs', 'year_of_release'
        )
