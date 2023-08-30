import datetime as dt

from rest_framework import serializers

from titles.models import Categories, Genres, Titles, TitlesGenre


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genres


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
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
