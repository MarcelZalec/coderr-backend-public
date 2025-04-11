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


class IsCustomer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE'] and request.user.is_superuser:
            return True
        if request.method == 'GET':
            return IsAuthenticated()
        if request.method in ['PATCH', 'POST', 'DELETE'] and request.user.profile.type == "customer" and request.user == obj.reviewer:
            return True
        return False