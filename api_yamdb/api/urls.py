from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriesViewSet,
    CommentsViewSet,
    GenresViewSet,
    GetTokenView,
    ReviewsViewSet,
    SignUpView,
    TitlesViewSet,
    UserViewSet,
)

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentsViewSet,
    basename='comment',
)
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/',
        include(
            [
                path('signup/', SignUpView.as_view()),
                path('token/', GetTokenView.as_view()),
            ]
        ),
    ),
]
