from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
]
