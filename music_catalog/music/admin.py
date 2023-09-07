from django.contrib import admin

from .models import Musician, Album, Song


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    ...


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    ...


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    ...
