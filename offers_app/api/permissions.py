from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

class OfferPermission(BasePermission):
    """
    Custom permission class for Offer-related actions.

    Methods:
    - has_permission(request, view): Defines access rules for different request methods.
    - has_object_permission(request, view, obj): Checks object-level permissions.

    Rules:
    - GET requests: Allowed for all users.
    - Authenticated users:
        - PATCH, POST, DELETE: Allowed only for business users.
        - Others: Denied.
    - Object-level permissions:
        - Allowed if the requester is the owner or authenticated.

    Returns:
    - Boolean indicating whether the request is permitted.
    """
    def has_permission(self, request, view):
        
        if request.method == 'GET':
            return True
        
        if not request.user.is_authenticated:
            return False
        
        if request.method in ['PATCH', 'POST', 'DELETE'] and request.user.profile.type == 'business':
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_authenticated:
            return True
        return False