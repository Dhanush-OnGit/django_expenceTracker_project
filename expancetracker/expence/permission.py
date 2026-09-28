from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Only non admin user are allowed"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff == False)