from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    """Проверка на залогиненного пользователя"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorAdminSuperuserOrReadOnlyPermission(permissions.BasePermission):
    """Проверка, является ли пользователь админом, модером или автором объекта."""

    message = (
        'Проверка пользователя является ли он администрацией'
        'или автором объекта, иначе только режим чтения'
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
    """ "Проверка прав админа."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
