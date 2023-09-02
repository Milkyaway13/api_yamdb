import datetime as dt

from rest_framework import serializers

from titles.models import Categories, Genres, Titles
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий'''

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров'''

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genres


class CategoryField(serializers.SlugRelatedField):
    '''Кастомное слаг поле категории'''

    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class GenreField(serializers.SlugRelatedField):
    '''Кастомное слаг поле жанра'''

    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
    '''Сериализатор для тайтлов'''

    genre = GenreField(
        slug_field='slug', queryset=Genres.objects.all(), many=True
    )
    category = CategoryField(
        slug_field='slug', queryset=Categories.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Titles

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год фильма не может быть больше текущего!'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для информации о пользователях.'''

    class Meta:
        class Meta:
            model = User
            fields = (
                'username',
                'email',
                'first_name',
                'last_name',
                'bio',
                'role',
            )


class TokenSerializer(serializers.ModelSerializer):
    '''Сериализатор для токенов.'''

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания пользователя.'''

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
        return value
