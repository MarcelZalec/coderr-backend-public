from django.urls import path, include
from .views import BaseInfoView
from auth_app.api.views import CustomLoginView, RegistrationView
from offers_app.api.views import SingleOfferDetailView
from profile_app.api.views import UserProfileDetail
from orders_app.api.views import OrderCountAPIView, CompletedOrderCount

urlpatterns = [ 
    path('offers/', include('offers_app.api.urls')), 
    path('offerdetails/<int:pk>/', SingleOfferDetailView.as_view(), name='offerdetails-detail'),
    path('orders/', include('orders_app.api.urls')),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
    path('order-count/<int:business_user_id>/', OrderCountAPIView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCount.as_view(), name='completed-order-count'),
    path('profiles/', include('profile_app.api.urls')),
    path('profile/<int:user>/', UserProfileDetail.as_view(), name='profile-detail'),
    path('reviews/', include('reviews_app.api.urls')),
    path('login/', CustomLoginView.as_view()),
    path('registration/', RegistrationView.as_view()),
]