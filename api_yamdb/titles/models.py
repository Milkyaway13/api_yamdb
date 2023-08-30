from django.db import models


class Genres(models.Model):
    name = models.CharField('Имя жанра', max_length=20)
    slug = models.SlugField('Ссылка на жанры', unique=True, max_length=20)

    def __str__(self) -> str:
        return self.name


class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Ссылка на категорию', unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Titles(models.Model):
    name = models.CharField('Название произведения', max_length=500)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genres, verbose_name='Жанры', through='TitlesGenre'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='titles',
    )

    def __str__(self) -> str:
        return self.name


class TitlesGenre(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
