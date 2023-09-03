import datetime as dt

from rest_framework import serializers

from titles.models import (
    Categories,
    Comments,
    Genres,
    Reviews,
    Titles,
    TitlesGenre
)


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

class CommentsSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class ReviewsSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('text', 'score')
        model = Reviews
