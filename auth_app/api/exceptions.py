from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    print(f"exeptions wird ausgeführt......................................{isinstance(exc, NotAuthenticated)}")
    response = exception_handler(exc, context)

    # Falls kein Token vorhanden ist oder der Benutzer nicht authentifiziert ist
    if isinstance(exc, NotAuthenticated):
        return Response({"error": "Authentifizierung erforderlich. Bitte einen gültigen Token übermitteln."}, 
                        status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, AuthenticationFailed):
        return Response({"error": "Token ist ungültig oder abgelaufen."}, 
                        status=status.HTTP_401_UNAUTHORIZED)

    return response  # Standardmäßige Fehlerbehandlung