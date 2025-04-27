from rest_framework import generics, mixins, viewsets, filters, status
from offers_app.models import Offer, OfferDetails
from .serializer import *
from .pagination import ResultPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter
from auth_app.api.permissions import IsAuthenticated
from .permissions import OfferPermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling offers with filtering, search, pagination, and permissions.

    Attributes:
    - queryset: Retrieves all Offer instances.
    - filter_backends: Enables filtering, search, and ordering capabilities.
    - filterset_class: Uses OfferFilter to filter results.
    - search_fields: Allows search based on 'title' and 'description'.
    - ordering_fields: Enables ordering by 'min_price' and 'updated_at'.
    - pagination_class: Uses ResultPagination for paginated responses.
    - permission_classes: Applies OfferPermission rules.
    - authentication_classes: Requires TokenAuthentication.

    Methods:
    - get_serializer_class(): Dynamically selects serializer based on action.
    - perform_create(serializer): Ensures exactly three details are provided when creating an offer.

    Raises:
    - NotFound: If offer details count is not exactly 3.
    """
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    pagination_class = ResultPagination
    permission_classes = [OfferPermission]
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action == 'list':
            return OffersListSerializer
        elif self.action == 'create':
            return OfferWriteSerializer
        elif self.action == 'retrieve':
            return SingleOfferListSerializer
        elif self.action == 'partial_update':
            return OfferWriteSerializer
        elif self.action == 'destroy':
            return SingleOfferListSerializer
        return OfferWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting OfferDetails.

    Attributes:
    - queryset: Retrieves all OfferDetails instances.
    - serializer_class: Uses OfferDetailSerializer.
    - permission_classes: Requires user authentication.
    - authentication_classes: Uses TokenAuthentication.
    """
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class OffersView(viewsets.ModelViewSet):
    """
    ViewSet for handling Offer instances with basic authentication.

    Attributes:
    - queryset: Retrieves all Offer instances.
    - authentication_classes: Uses TokenAuthentication.
    - serializer_class: Uses OffersXXSerializer.
    """
    queryset = Offer.objects.all()
    authentication_classes= [TokenAuthentication]
    serializer_class = OffersXXSerializer