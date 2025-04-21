from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

class OrderPermission(BasePermission):
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
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False