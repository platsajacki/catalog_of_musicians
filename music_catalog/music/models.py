import datetime as dt

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator

from constants import SONGS_IN_ALBUM
from core.models import NameSlugField

User: AbstractBaseUser = get_user_model()


class Musician(NameSlugField, models.Model):
    """Модель для представления исполнителей."""
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['name']


class Song(NameSlugField, models.Model):
    """Модель для представления песен."""
    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'
        ordering = ['name']


class Album(NameSlugField, models.Model):
    """Модель для представления музыкальных альбомов."""
    musician = models.ForeignKey(
        Musician, related_name='albums',
        verbose_name='Исполнитель',
        on_delete=models.CASCADE
    )
    year_of_release = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(dt.datetime.now().year)
        ],
        verbose_name='Год выпуска'
    )
    songs = models.ManyToManyField(
        Song,
        through='AlbumSong',
        related_name='albums',
        verbose_name='Песни в альбоме'
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
    number_in_album = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(SONGS_IN_ALBUM)
        ],
        verbose_name='Порядковый номер в альбоме'
    )

    class Meta:
        verbose_name = 'Песня в альбоме'
        verbose_name_plural = 'Песни в альбомах'
        unique_together = [
            ['album', 'song', 'number_in_album'],
            ['album', 'number_in_album']
        ]
        ordering = ['number_in_album']
