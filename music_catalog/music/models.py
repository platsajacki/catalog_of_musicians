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


class Song(NameField, models.Model):
    """Модель для представления песен."""
    musician = models.ManyToManyField(
        Musician, related_name='songs',
        verbose_name='Исполнитель'
    )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'
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


class AlbumSong(models.Model):
    """
    Модель для связи альбомов и песен
    с указанием порядкового номера песни в альбоме.
    """
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Альбом'
    )
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE,
        related_name='songs',
        verbose_name='Песня'
    )
    number = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(SONGS_IN_ALBUM)
        ],
        verbose_name='Порядковый номер в альбоме'
    )

    class Meta:
        verbose_name = 'Песня в альбоме'
        verbose_name_plural = 'Песни в альбомах'
        unique_together = ['album', 'song']
        ordering = ['number']
