from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    CategoriesViewSet,
    CommentsViewSet,
    GenresViewSet,
    ReviewsViewSet,
    TitlesViewSet,
)

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentsViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
]
