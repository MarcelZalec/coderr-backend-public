from django.contrib import admin
from profile_app.models import UserProfile
from orders_app.models import Order
from offers_app.models import Offer

    
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Offer)