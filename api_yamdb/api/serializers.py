from rest_framework import serializers
from titles.models import Categories
import datetime as dt

from titles.models import (
    Categories,
    Comments,
    Genres,
    Reviews,
    Titles,
    TitlesGenre
)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genres = GenresSerializer(many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        title = Titles.objects.create(**validated_data)

        for genre in genres:
            slug, name = Genres.objects.get(slug=genre['slug'])
            TitlesGenre.objects.create(title=title, genre=slug)

        return title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год фильма не может быть больше текущего!'
            )
        return value

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ['titles', ]


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ['titles', ]
