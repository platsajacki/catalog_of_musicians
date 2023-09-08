from django.db import models


class NameSlugField(models.Model):
    """
    Абстрактная модель, включающая в себя поля 'slug',
    'name' и cтроковое представление 'name'.
    """
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('Слаг', max_length=150, unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Возвращает строковое представление 'name'."""
        return self.name
