from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated
from django.contrib.auth.models import AnonymousUser


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
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
    
    
class standardPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return [AllowAny()]
        return False
        
        
class SetStandardPermission(BasePermission):
    """
    Standardberechtigungen für verschiedene HTTP-Methoden.
    - GET: Authentifizierte Nutzer dürfen lesen.
    - POST: Nur Geschäftsbenutzer dürfen schreiben.
    - PATCH/DELETE: Nur Eigentümer oder Admins dürfen ändern/löschen.
    """

    def has_permission(self, request, view):
        """Überprüft die Berechtigung auf View-Ebene."""
        # if isinstance(request.user, AnonymousUser):
        #     return False  # Nicht authentifizierte Nutzer haben keinen Zugriff.
        
        if request.method == 'GET':
            return [AllowAny()]

        if request.method == 'POST':
            return IsBusinessUser().has_permission(request, view)  # Nur Geschäftsbenutzer.

        if request.method in ['PATCH', 'DELETE']:
            return IsOwnerOrAdmin().has_permission(request, view)  # Nur Eigentümer/Admins.

        return True  # Standard: Authentifizierte Nutzer dürfen GET-Anfragen ausführen.

    def has_object_permission(self, request, view, obj):
        """Überprüft die Berechtigung auf Objekt-Ebene."""
        if request.method in ['PATCH', 'DELETE']:
            return bool(request.user == obj.user or request.user.is_superuser)
        
        return True  # Falls `has_permission()` bestanden wurde, gibt es hier keine weiteren Einschränkungen.


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['DELETE'] and request.user.is_superuser:
            return True
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'POST', 'DELETE'] and request.user.profile.type == "customer" and request.user == obj.reviewer:
            return True
        return False
    
    
    # ⚠️