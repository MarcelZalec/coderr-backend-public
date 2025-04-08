from rest_framework import generics, mixins
from offers_app.models import Offer, OfferDetails
from .serializer import SingleOfferListSerializer, OfferWriteSerializer, OffersListSerializer, OfferDetailSerializer, GetOfferSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
# from .pagination import ResultsSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter
from auth_app.api.permissions import *
from rest_framework.viewsets import GenericViewSet

class OfferViewSet(GenericViewSet):
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    #pagination_class = ResultsSetPagination
    permission_classes = [IsOwnerOrAdmin]

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
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [setStandartPermission]