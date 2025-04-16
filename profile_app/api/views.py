from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from profile_app.models import UserProfile
from .serializers import *
from auth_app.api.permissions import *
from auth_app.api.permissions import IsOwnerOrAdmin


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = "user"


class BusinessProfileView(APIView):
    """
    API endpoint for retrieving all business user profiles.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        Retrieve all business user profiles.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized business user profiles.
        """
        users = UserProfile.objects.filter(type='business')
        serializer = BusinessUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    """
    API endpoint for retrieving the profile of the authenticated user.

    Only accessible to authenticated users.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Retrieve the profile of the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the serialized user data if found.
            Response: A JSON response with an error message if the user is not found.
        """
        try:
            user = UserProfile.objects.filter(type='customer') # .get(pk=request.user.id)
            serializer = CustomerUserSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "Benutzerprofil nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND,
            )