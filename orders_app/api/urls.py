from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    # path('order-count/<int:business_user>/', OrderCountAPIView.as_view(), name='order-count'),
    # path('completed-order-count/<int:business_user>/', GetCompletedOrderView.as_view(), name='completed-order-count'),
]