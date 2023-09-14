import datetime as dt

from django.core.exceptions import ValidationError


def validate_username_field(value):
    if value == 'me':
        raise ValidationError('Имя пользователя "me" запрещено.')


def validate_year_field(value):
    if value > dt.date.today().year:
        raise ValidationError('Год фильма не может быть больше текущего!')
