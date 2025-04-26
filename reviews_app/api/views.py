from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from auth_app.api.permissions import IsCustomer, AllowAny, IsAuthenticated
from reviews_app.models import Reviews
from .serializer import ReviewsSerializer, ReviewsPOSTSerializer
from rest_framework.authentication import TokenAuthentication


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling reviews with authentication, filtering, and ordering.
    """
    
    queryset = Reviews.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated ,IsCustomer]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['rating', 'updated_at']
    filterset_fields = ['business_user_id', 'reviewer_id']
    pagination_class = None
    
    def get_serializer_class(self):
        """
        Determines the appropriate serializer based on the action.

        Returns:
        - ReviewsSerializer for 'list' and 'retrieve'.
        - ReviewsPOSTSerializer for other actions.
        """
        if self.action in ['list', 'retrieve']:
            return ReviewsSerializer
        return ReviewsPOSTSerializer
    
    
    def perform_create(self, serializer):
        """
        Ensures that the authenticated user is set as the reviewer when a new review is created.

        Parameters:
        - serializer: The serializer instance for validation and saving.
        """
        serializer.save(reviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handles review creation and returns a formatted response.

        Parameters:
        - request: The HTTP request object.
        - *args, **kwargs: Additional parameters for handling request.

        Returns:
        - Response: Serialized review data upon successful creation (HTTP_201_CREATED).
        - Response: Validation errors if data is invalid (HTTP_400_BAD_REQUEST).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(reviewer=self.request.user)

        output_serializer = ReviewsSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """
        Handles partial updates for reviews and returns formatted response.

        Parameters:
        - request: The HTTP request object.
        - *args, **kwargs: Additional parameters for handling request.

        Returns:
        - Response: Updated review data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        output_serializer = ReviewsSerializer(instance)
        return Response(output_serializer.data)