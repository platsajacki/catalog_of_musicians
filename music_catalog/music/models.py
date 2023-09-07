import datetime as dt

from django.db import models
from django.core.validators import MaxValueValidator

from constants import SONGS_IN_ALBUM
from core.models import NameField


class Musician(NameField, models.Model):
    """Модель для представления исполнителей."""
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['name']


class Album(NameField, models.Model):
    """Модель для представления музыкальных альбомов."""
    musician = models.ManyToManyField(
        Musician, related_name='albums',
        verbose_name='Исполнитель'
    )
    year_of_release = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(dt.datetime.now().year)
        ],
        verbose_name='Год выпуска'
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['name', '-year_of_release']


class Song(NameField, models.Model):
    """Модель для представления песен."""
    album = models.ManyToManyField(
        Album, related_name='songs',
        verbose_name='Альбом'
    )
    number = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(SONGS_IN_ALBUM)
        ],
        verbose_name='Порядковый номер в альбоме'
    )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'
        ordering = ['name', 'number']
