from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from api.permissions import (
    IsAdminUserOrReadOnly,
    IsAuthorAdminSuperuserOrReadOnlyPermission,
)
from api.serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
)
from titles.models import Categories, Genres, Titles


class CategoriesViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    '''Вьюсет для категорий'''

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = IsAdminUserOrReadOnly


class GenresViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    '''Вьюсет для жанров'''

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = IsAdminUserOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    '''Вьюсет для тайтлов'''

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = IsAuthorAdminSuperuserOrReadOnlyPermission

    def update(self, request, *args, **kwargs):
        return Response(
            'Метод PUT запрещен!', status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = TitlesSerializer(
            get_object_or_404(self.queryset, id=self.kwargs.get('pk')),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
