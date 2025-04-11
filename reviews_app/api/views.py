from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from auth_app.api.permissions import IsCustomer, AllowAny
from reviews_app.models import Reviews
from .serializer import ReviewsSerializer, ReviewsPOSTSerializer
from rest_framework.authentication import TokenAuthentication


class ReviewViewSet(viewsets.ModelViewSet):
    
    queryset = Reviews.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['rating', 'updated_at']
    filterset_fields = ['business_user_id', 'reviewer_id']
    pagination_class = None
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewsSerializer
        return ReviewsPOSTSerializer
    
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(reviewer=self.request.user)

        output_serializer = ReviewsSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        output_serializer = ReviewsSerializer(instance)
        return Response(output_serializer.data)