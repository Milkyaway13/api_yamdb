from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, filters
from api.serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
)
from rest_framework import status
from titles.models import Categories, Genres, Titles
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


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


class TitlesViewSet(
    viewsets.ViewSet,
    viewsets.GenericViewSet,
):
    queryset = Titles.objects.all()
    pagination_class = PageNumberPagination

    def get_title(self, queryset, pk):
        return get_object_or_404(queryset, id=pk)

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = TitlesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TitlesSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TitlesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        serializer = TitlesSerializer(self.get_title(self.queryset, pk))
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        serializer = TitlesSerializer(
            self.get_title(self.queryset, pk), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.get_title(self.queryset, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
