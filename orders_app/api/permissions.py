from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

class OrderPermission(BasePermission):
    """
    Custom permission class for managing order-related actions.

    Methods:
    - has_permission(request, view): Defines general access rules.
    - has_object_permission(request, view, obj): Defines object-level access rules.

    Rules:
    - Authentication:
        - Users must be authenticated to proceed.
    - Request Permissions:
        - GET: Allowed if user is authenticated.
        - POST: Allowed if user is a customer.
        - PATCH: Allowed if user is a business.
    - Object-Level Permissions:
        - PATCH: Allowed only if the user is a business and owns the object.

    Returns:
    - Boolean indicating whether the request is permitted.
    """
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return NotAuthenticated({'error': 'Benutzer ist nicht authentifiziert.'})
        
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        if request.method == 'POST' and request.user.profile.type == "customer":
            return True
        if request.method == 'PATCH' and request.user.profile.type == "business":
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH' and request.user.profile.type == "business" and request.user == obj.user:
            return True
        return False
    

class ViewCounts(BasePermission):
    """
    Permission class to allow authenticated users to access view counts.

    Methods:
    - has_permission(request, view): Checks authentication status.

    Returns:
    - True if the user is authenticated.
    - False otherwise.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False