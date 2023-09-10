from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    """Проверка на залогиненного пользователя."""

    message = "Доступ разрешен только для авторизованных пользователей."

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorAdminSuperuserOrReadOnlyPermission(permissions.BasePermission):
    """
    Проверка, является ли пользователь админом,
    модером или автором объекта.
    """

    message = (
        "Доступ разрешен только для администраторов,"
        "модераторов и авторов объекта."
    )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdminPermission(BasePermission):
    """Проверка прав админа."""

    message = "У вас нет прав администратора"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnlyPermisson(BasePermission):
    """
    Проверка, является ли пользователь админом,
    модером или суперюзером.
    """

    message = (
        "Доступ разрешен только для администраторов,"
        "модераторов и суперюзеров"
    )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_admin or request.user.is_moderator
        )
