from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'author'):
            return False
        user = request.user
        return user.is_staff or obj.author.pk == user.pk


class OwnerOrAdminOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'author'):
            return False
        user = request.user
        if obj.author.pk == user.pk:
            return True
        return request.method in SAFE_METHODS or user.is_staff


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
