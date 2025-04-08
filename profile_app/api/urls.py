from django.urls import path, include
from .views import BusinessProfileView, CustomerProfileView

urlpatterns = [
    path('business/', BusinessProfileView.as_view(), name='profiles-business-list'),
    path('customer/', CustomerProfileView.as_view(), name='profiles-customer-list')       
]