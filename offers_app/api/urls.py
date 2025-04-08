from django.urls import path, include
# from .views import *
from .views2 import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', OfferViewSet, basename='offers')

urlpatterns = [
    path('', include(router.urls)),
]