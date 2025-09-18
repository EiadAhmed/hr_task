from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHR(BasePermission):
    """
    Custom permission to only allow HR users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser can do anything
        if request.user.is_superuser:
            return True
        
        # Check if user has an associated employee with HR designation
        print(request.user.employee.designation)
        try:
            return request.user.employee.designation == 'hr'
        except:
            return False


class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)