from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django_filters import rest_framework
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (
    IsAdminUserOrReadOnly,
    IsAuthorAdminSuperuserOrReadOnlyPermission,
    IsAdminPermission,
    IsAdminOrReadOnlyPermisson,
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
from reviews.models import Category, Genre, Title, Review
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

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = (IsAdminUserOrReadOnly,)


class GenresViewSet(
    ListCreateDestroyMixins,
):
    '''Вьюсет для жанров'''

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = (IsAdminUserOrReadOnly,)


class TitleFilter(rest_framework.FilterSet):
    genre = rest_framework.CharFilter(field_name='genre', lookup_expr='slug')
    category = rest_framework.CharFilter(
        field_name='category', lookup_expr='slug'
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
        )


class TitlesViewSet(viewsets.ModelViewSet):
    '''Вьюсет для тайтлов'''

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnlyPermisson,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )


class CommentsViewSet(viewsets.ModelViewSet):
    '''Вьюсет для комментариев'''

    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorAdminSuperuserOrReadOnlyPermission,)
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_obj(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('reviews_id'),
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )

    def get_queryset(self):
        return self.get_obj().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_obj())


class ReviewsViewSet(viewsets.ModelViewSet):
    '''Вьюсет для отзывов'''

    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorAdminSuperuserOrReadOnlyPermission,)
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_obj(self, model):
        return get_object_or_404(model, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_obj(Title).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_obj(Title))
    

    def create(self, request, *args, **kwargs):
        if len(self.get_obj(Title).reviews.filter(author=self.request.user)):
            return Response(
                'Нельзя оценить одно произведение дважды!',
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


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
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            return Response(
                'Такой логин или email уже существуют',
                status=status.HTTP_400_BAD_REQUEST,
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


class GetTokenView(APIView):
    """Вьюшка для получения JWT-токена."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Неверный код')
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def about_me(self, request):
        if request.method == 'PATCH':
            serializer = UserCreateSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserCreateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
