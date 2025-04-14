from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderViewSet.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderViewSet.as_view(), name='order-detail'),
]