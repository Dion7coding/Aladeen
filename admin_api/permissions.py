from rest_framework.permissions import BasePermission


class IsAdminUserOnly(BasePermission):
    """
    Allows access only to admin (staff) users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
