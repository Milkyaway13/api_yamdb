from rest_framework import serializers


def validate_username_field(value):
    if value == 'me':
        raise serializers.ValidationError('Имя пользователя "me" запрещено.')
