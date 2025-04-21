from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

class OfferPermission(BasePermission):
    def has_permission(self, request, view):
        
        if request.method == 'GET':
            return True
        
        if request.method in ['PATCH', 'POST', 'DELETE'] and request.user.profile.type == 'business':
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_authenticated:
            return True
        return False