from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler for authentication errors in Django REST Framework.

    Parameters:
    exc (Exception): The raised exception.
    context (dict): Context of the request where the exception occurred.

    Functionality:
    1. Prints a debug statement to check if 'NotAuthenticated' exception is raised.
    2. Calls the standard DRF exception handler.
    3. Handles specific authentication issues:
       - If 'NotAuthenticated': Returns HTTP 401 with an error message.
       - If 'AuthenticationFailed': Returns HTTP 401 with an error message.
    4. Returns the standard response if no specific cases apply.

    Returns:
    Response: A customized error response or the default response.
    """
    response = exception_handler(exc, context)

    # Falls kein Token vorhanden ist oder der Benutzer nicht authentifiziert ist
    if isinstance(exc, NotAuthenticated):
        return Response({"error": "Authentifizierung erforderlich. Bitte einen gültigen Token übermitteln."}, 
                        status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, AuthenticationFailed):
        return Response({"error": "Token ist ungültig oder abgelaufen."}, 
                        status=status.HTTP_401_UNAUTHORIZED)

    return response  # Standardmäßige Fehlerbehandlung