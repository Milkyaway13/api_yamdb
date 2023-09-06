from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (
    IsAdminUserOrReadOnly,
    IsAuthorAdminSuperuserOrReadOnlyPermission,
    IsAdminPermission,
)
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitlesSerializer,
    UserSerializer,
    UserCreateSerializer,
    TokenSerializer,
)
from titles.models import Categories, Genres, Titles
from users.models import User


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
    permission_classes = (IsAuthorAdminSuperuserOrReadOnlyPermission, )
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class ReviewsViewSet(viewsets.ModelViewSet):
    '''Вьюсет для отзывов'''

    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorAdminSuperuserOrReadOnlyPermission, )
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class GetTokenView(APIView):
    """Вьюшка для получения JWT-токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Неверный код')
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    '''Вьюшка для авторизации'''
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """Создание пользователя И Отправка письма с кодом."""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data)
        except IntegrityError:
            return Response(
                'Такой логин или email уже существуют',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.AUTH_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name='me', permission_classes=(permissions.IsAuthenticated,))
    def about_me(self, request):
        if request.method == 'PATCH':
            serializer = UserCreateSerializer(
                request.user, data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserCreateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
