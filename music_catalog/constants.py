from drf_spectacular.utils import extend_schema

SONGS_IN_ALBUM: int = 50

DESCRIPTION_PROJECT = (
    'Проект Django Rest Framework (DRF) представляет собой веб-приложение '
    'для управления информацией о музыкальных исполнителях, их альбомах и '
    'содержащихся в них песнях.'
)

MUSICIAN_SCHEMA: dict[str, extend_schema] = {
    'list': extend_schema(
        summary='Получить всех исполнителей.',
        description=(
            'Получить информацию об исполнителях музыки. '
            'Доступно всем пользователям.'
        ),
    ),
    'create': extend_schema(
        summary='Создать исполнителя.',
        description=(
            'Создать информацию о исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
    'retrieve': extend_schema(
        summary='Получить исполнителя.',
        description=(
            'Получить информацию о конкретном исполнителе музыки. '
            'Доступно всем пользователям.'
        ),
    ),
    'update': extend_schema(
        summary='Обновить информацию исполнителя.',
        description=(
            'Обновить информацию о конкретном исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
    'partial_update': extend_schema(
        summary='Частично обновить информацию исполнителя.',
        description=(
            'Частично обновить информацию о конкретном исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
    'destroy': extend_schema(
        summary='Удалить информацию об исполнителе.',
        description=(
            'Удалить информацию о конкретном исполнителе музыки. '
            'Доступно только администратору.'
        ),
    ),
}

SONG_SCHEMA: dict[str, extend_schema] = {
    'list': extend_schema(
        summary='Получить все музыкальные произведения.',
        description=(
            'Получить информацию о музыкальных произведениях. '
            'Доступно всем пользователям.'
        ),
    ),
    'create': extend_schema(
        summary='Создать музыкальное произведение.',
        description=(
            'Создать информацию о музыкальном произведении. '
            'Доступно только администратору.'
        ),
    ),
    'retrieve': extend_schema(
        summary='Получить музыкальное произведение.',
        description=(
            'Получить информацию о конкретном музыкальном произведении. '
            'Доступно всем пользователям.'
        ),
    ),
    'update': extend_schema(
        summary='Обновить информацию о музыкальном произведении.',
        description=(
            'Обновить информацию о конкретном музыкальном произведении. '
            'Доступно только администратору.'
        ),
    ),
    'partial_update': extend_schema(
        summary='Частично обновить информацию о музыкальном произведении.',
        description=(
            'Частично обновить информацию о конкретном музыкальном '
            'произведении. Доступно только администратору.'
        ),
    ),
    'destroy': extend_schema(
        summary='Удалить информацию о музыкальном произведении.',
        description=(
            'Удалить информацию о конкретном музыкальном произведении. '
            'Доступно только администратору.'
        ),
    ),
}

ALBUM_SCHEMA: dict[str, extend_schema] = {
    'list': extend_schema(
        summary='Получить все альбомы.',
        description=(
            'Получить информацию о всех альбомах. '
            'Доступно всем пользователям.'
        ),
    ),
    'create': extend_schema(
        summary='Создать альбом.',
        description=(
            'Создать информацию о новом альбоме. '
            'Доступно только администратору.'
        ),
    ),
    'retrieve': extend_schema(
        summary='Получить альбом.',
        description=(
            'Получить информацию о конкретном альбоме. '
            'Доступно всем пользователям.'
        ),
    ),
    'update': extend_schema(
        summary='Обновить информацию о альбоме.',
        description=(
            'Обновить информацию о конкретном альбоме. '
            'Доступно только администратору.'
        ),
    ),
    'partial_update': extend_schema(
        summary='Частично обновить информацию о альбоме.',
        description=(
            'Частично обновить информацию о конкретном альбоме. '
            'Доступно только администратору.'
        ),
    ),
    'destroy': extend_schema(
        summary='Удалить альбом.',
        description=(
            'Удалить информацию о конкретном альбоме. '
            'Доступно только администратору.'
        ),
    ),
}
