from django.db import models


class NameField(models.Model):
    """
    Абстрактная модель, включающая в себя поле
    'name' и его строковое представление.
    """
    name = models.CharField('Название', max_length=150)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Возвращает строковое представление 'name'."""
        return self.name
