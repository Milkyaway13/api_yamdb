from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets

from api.permissions import (
    IsAdminUserOrReadOnly,
    IsAuthorAdminSuperuserOrReadOnlyPermission,
)
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitlesSerializer,
)
from titles.models import Categories, Genres, Titles


class ListCreateDestroyMixins(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    pass


class CategoriesViewSet(ListCreateDestroyMixins):
    '''Вьюсет для категорий'''

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = (IsAdminUserOrReadOnly,)


class GenresViewSet(
    ListCreateDestroyMixins,
):
    '''Вьюсет для жанров'''

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = (IsAdminUserOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    '''Вьюсет для тайтлов'''

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthorAdminSuperuserOrReadOnlyPermission,)
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )


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
