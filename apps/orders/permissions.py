from rest_framework import permissions
from apps.accounts.constants import UserRole

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and request.user.role == UserRole.ADMIN
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.client == request.user
