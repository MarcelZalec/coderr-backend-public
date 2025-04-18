from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        print(request.user.profile.type)
        if not request.user or not request.user.profile.type == "business":
            # raise AuthenticationFailed()
            raise PermissionDenied({"error": "Authentifizierter Benutzer ist nicht der Eigentümer des Angebots"})
        return True


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        elif request.method in ["PATCH", "DELETE"]:
            return bool(request.user == obj.user)
        return False
        
        
class SetStandardPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("⚠️ Permission überprüft!"f"{request.user and request.user.is_authenticated}")
        if not request.user.is_authenticated:
            return NotAuthenticated({'error': 'Benutzer ist nicht authentifiziert.'})
        if request.method == 'GET':
            if request.user and request.user.is_authenticated:
                return True
            else:
                raise PermissionDenied({"error": "Benutzer ist nicht authentifiziert."})  # 403

        if request.method == 'POST':
            print(IsBusinessUser().has_object_permission(request, view, obj))
            if IsBusinessUser().has_object_permission(request, view, obj) and request.user.is_authenticated:
                return True
            else:
                raise PermissionDenied({"error": "Benutzer ist nicht berechtigt."})  # 403

        if request.method in ['PATCH', 'DELETE']:
            if IsOwnerOrAdmin().has_object_permission(request, view, obj) and request.user.is_authenticated:
                return True
            else:
                raise PermissionDenied({"error": "Nur Eigentümer oder Admins erlaubt."})  # 403

        raise PermissionDenied({"error": "Ungültige Anfrage."})  # 403 für alle unbekannten Methoden


class IsCustomer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE'] and request.user.is_superuser:
            return True
        if request.method == 'GET':
            return IsAuthenticated()
        if request.method in ['PATCH', 'POST', 'DELETE'] and request.user.profile.type == "customer" and request.user == obj.reviewer:
            return True
        return False