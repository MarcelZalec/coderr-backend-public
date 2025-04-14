from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderViewSetff.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderViewSetff.as_view(), name='order-detail'),
]