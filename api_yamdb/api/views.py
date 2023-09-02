from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, filters
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitlesSerializer,
)
from rest_framework import status
from titles.models import Categories, Genres, Titles
from rest_framework.response import Response


class CategoriesViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class GenresViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class TitlesViewSet(viewsets.ViewSet):
    queryset = Titles.objects.all()

    def get_title(self, queryset, slug):
        return get_object_or_404(queryset, slug)

    def list(self, request):
        serializer = TitlesSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TitlesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, slug=None):
        serializer = TitlesSerializer(data=self.get_title(self.queryset, slug))
        return Response(serializer.data)

    def partial_update(self, request, slug=None):
        serializer = TitlesSerializer(
            Titles, data=self.get_title(self.queryset, slug), partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, slug=None):
        self.get_title(self.queryset, slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsViewSet(viewsets.ModelViewSet):
    '''Вьюсет для комментариев'''
    serializer_class = CommentsSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class ReviewsViewSet(viewsets.ModelViewSet):
    '''Вьюсет для отзывов'''
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
