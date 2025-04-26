from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated


class IsBusinessUser(BasePermission):
    """
    Permission class to ensure that the authenticated user is a business owner.

    Methods:
    - has_permission(request, view): Checks if the user is a business.

    Raises:
    - PermissionDenied: If the user is not a business owner.
    """
    def has_permission(self, request, view):
        print(request.user.profile.type)
        if not request.user or not request.user.profile.type == "business":
            # raise AuthenticationFailed()
            raise PermissionDenied({"error": "Authentifizierter Benutzer ist nicht der Eigentümer des Angebots"})
        return True


class IsOwnerOrAdmin(BasePermission):
    """
    Permission class to allow only owners or admins to edit or delete objects.

    Methods:
    - has_object_permission(request, view, obj): Checks object-level permissions.

    Returns:
    - True: If user is authenticated and owner/admin.
    - False: Otherwise.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        elif request.method in ["PATCH", "DELETE"]:
            return bool(request.user == obj.user)
        return False
        
        
class SetStandardPermission(BasePermission):
    """
    Standard permission class for general request validation.

    Methods:
    - has_object_permission(request, view, obj): Checks user authentication and permissions.

    Raises:
    - NotAuthenticated: If user is not authenticated.
    - PermissionDenied: If user lacks the required permissions.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return NotAuthenticated({'error': 'Benutzer ist nicht authentifiziert.'})
        if request.method == 'GET':
            if request.user and request.user.is_authenticated:
                return True
            else:
                raise PermissionDenied({"error": "Benutzer ist nicht authentifiziert."})  # 403

        if request.method == 'POST':
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
    """
    Permission class to ensure customer-based authorization.

    Methods:
    - has_permission(request, view): Checks request-level permissions.
    - has_object_permission(request, view, obj): Checks object-level permissions.

    Raises:
    - NotAuthenticated: If user is not authenticated.
    - PermissionDenied: If user lacks necessary permissions.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated({'error': 'Benutzer ist nicht authentifiziert.'})
        if request.method == 'GET':
            return True
        if request.method in ['DELETE'] and request.user.is_superuser:
            return True
        if request.method in ['PATCH', 'POST', 'DELETE'] and request.user.profile.type == "customer":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.reviewer or request.user.is_superuser:
            return True
        return False