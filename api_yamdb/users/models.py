from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
)


class User(AbstractUser):
    """Кастомная модель юзера."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        validators=[
            validators.RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username doesnt comply',
            ),
        ],
        max_length=150,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail',
        help_text='Укажите e-mail',
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=150, blank=True, null=True, verbose_name='Проверочный код'
    )
    first_name = models.CharField(
        max_length=150, verbose_name='Имя', help_text='Ваше Имя', blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Ваша Фамилия',
        blank=True,
    )
    bio = models.TextField(
        max_length=1000,
        verbose_name='Биография',
        help_text='Расскажите о себе',
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=USER_ROLE,
        default=USER,
        help_text='Пользователь',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    def __str__(self):
        return self.username
