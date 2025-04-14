from django.contrib import admin
from profile_app.models import UserProfile
from orders_app.models import Order

# Register your models here.
    
admin.site.register(UserProfile)
admin.site.register(Order)