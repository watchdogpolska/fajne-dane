from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    If use is not admin, they can still access data in READ-ONLY mode, if authenticated.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser
