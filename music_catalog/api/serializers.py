from rest_framework import serializers

from .mixins import LookUpSlugFieldMixin
from music.models import Musician


class MusicianSerializer(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """
    Сериализатор для информации об исполнителях.
    Поддерживает создание и обновление данных об исполнителях.
    """
    class Meta:
        model = Musician
        fields = ('name', 'slug')
