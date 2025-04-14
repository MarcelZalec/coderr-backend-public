from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetails


class Order(models.Model):
    
    ORDER_STATUS = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_orders")
    title = models.CharField(max_length=255, default="detail titel")
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"