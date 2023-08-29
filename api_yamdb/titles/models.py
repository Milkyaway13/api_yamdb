from django.db import models


class Genres(models.Model):
    name = models.CharField('Имя жанра', max_length=20)

    def __str__(self) -> str:
        return self.name


class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=50)

    def __str__(self) -> str:
        return self.name


class Titles(models.Model):
    name = models.CharField('Название произведения', max_length=500)
    genres = models.ManyToManyField(
        Genres, verbose_name='Жанры', related_name='titles'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='titles',
    )

    def __str__(self) -> str:
        return self.name
