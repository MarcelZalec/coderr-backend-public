from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.profile.type == "business":
            raise AuthenticationFailed()
        return True


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PATCH", "DELETE"]:
            return bool(request.user == obj.user)
        return False
    
    
class setStandartPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return AllowAny()
        if request.method == 'POST':
            return IsBusinessUser()
        if request.method in ['PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]