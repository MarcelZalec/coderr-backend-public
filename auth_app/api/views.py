from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from profile_app.models import UserProfile


class RegistrationView(APIView):
    """
    API endpoint for user registration.

    Attributes:
    - permission_classes (list): Allows any user to access.

    Methods:
    - post(request): Handles user registration.

    Returns:
    - Response: Contains user details and authentication token upon success.
    - Response: Returns validation errors if registration fails.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account, user_type = serializer.save()


            token, created = Token.objects.get_or_create(user=saved_account)


            UserProfile.objects.get_or_create(
                user=saved_account, username=saved_account.username, type=user_type,
                email=saved_account.email)

            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            data = serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


class CustomLoginView(ObtainAuthToken):
    """
    API endpoint for user authentication and token generation.

    Attributes:
    - permission_classes (list): Allows any user to access.

    Methods:
    - post(request): Authenticates user and provides authentication token.

    Returns:
    - Response: Contains user details and authentication token upon success.
    - Response: Returns validation errors if authentication fails.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer._validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }
        else:
            data = serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)