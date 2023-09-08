from django.contrib.auth import authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .mixins import LookUpSlugFieldMixin
from music.models import Musician, User


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
