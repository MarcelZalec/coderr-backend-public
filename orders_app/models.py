from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetails


class Order(models.Model):
    """
    Model representing an order between a customer and a business.

    Attributes:
    - ORDER_STATUS (list): Choices for order status (in_progress, completed, cancelled).
    - customer_user (ForeignKey): References the customer placing the order.
    - business_user (ForeignKey): References the business receiving the order.
    - title (CharField): Title of the order.
    - revisions (IntegerField): Number of revisions allowed.
    - delivery_time_in_days (IntegerField): Estimated delivery time in days.
    - price (DecimalField): Price of the order.
    - features (JSONField): List of features included in the order.
    - offer_type (CharField): Defines the type of offer the order is associated with.
    - status (CharField): Current status of the order.
    - created_at (DateTimeField): Timestamp for when the order was created.
    - updated_at (DateTimeField): Timestamp for when the order was last updated.

    Choices:
    - ORDER_STATUS: Defines available order statuses.

    Methods:
    - __str__(): Returns the title of the order as a string representation.
    """
    
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