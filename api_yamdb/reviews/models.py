from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from api.utils import validate_year_field


class Genre(models.Model):
    '''Модель жанров.'''

    name = models.CharField('Имя жанра', max_length=20)
    slug = models.SlugField('Ссылка на жанры', unique=True, max_length=20)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    '''Модель категорий.'''

    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Ссылка на категорию', unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    '''Модель тайтлов.'''

    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField(
        'Год выпуска', validators=(validate_year_field,)
    )
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанры', through='TitlesGenre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='titles',
    )

    def __str__(self) -> str:
        return self.name


class TitlesGenre(models.Model):
    '''Модель жанров.'''

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genres'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='titles'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    '''Модель отзывов.'''

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], blank=False
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title',
            ),
        )

    def __str__(self) -> str:
        return f'Отзыв {self.author} на {self.title.name}'


class Comment(models.Model):
    '''Модель комментов.'''

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self) -> str:
        return f'Комментарий {self.author} на {self.review}'
