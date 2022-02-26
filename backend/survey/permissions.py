from rest_framework.permissions import BasePermission


class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    The request is authenticated as a user, or is a create request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in ['POST', 'OPTIONS'] or
            request.user and
            request.user.is_authenticated
        )
