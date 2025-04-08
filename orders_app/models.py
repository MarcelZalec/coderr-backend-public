from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetails


class Order(models.Model):
    
    ORDER_STATUS = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    offerdetails = models.ForeignKey(OfferDetails, on_delete=models.CASCADE, related_name="orders")
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_orders")
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)