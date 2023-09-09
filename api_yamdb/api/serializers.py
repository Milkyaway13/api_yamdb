import datetime as dt

from rest_framework import serializers
from users.models import User

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class CategoriesSerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий'''

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров'''

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre


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
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = CategoryField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        model = Title
        read_only_fields = ('rating',)

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
        regex=r'^[\w.@+-]+\Z', max_length=150, required=True
    )

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев'''

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewsSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов'''

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'score',
            'pub_date',
        )
        model = Review
