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
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class OffersView(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    authentication_classes= [TokenAuthentication]
    serializer_class = OffersXXSerializer