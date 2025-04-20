from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', OfferViewSet, basename='offers')

urlpatterns = [
    # path('', include(router.urls)),
    path('', OfferAPIView.as_view(), name='offer-list'),
    path('<int:pk>/', OfferAPIView.as_view(), name='offer-detail'),
]