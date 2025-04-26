from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    """
    Model representing an offer created by a user.

    Attributes:
    - user (ForeignKey): References the creator of the offer.
    - title (CharField): The title of the offer.
    - image (FileField): Optional image associated with the offer.
    - description (CharField): A brief description of the offer.
    - created_at (DateTimeField): Timestamp for when the offer was created.
    - updated_at (DateTimeField): Timestamp for when the offer was last updated.

    Meta:
    - ordering: Orders offers alphabetically by title.

    Methods:
    - __str__(): Returns the title of the offer as a string representation.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/orders/', null=True, blank=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


class OfferDetails(models.Model):
    """
    Model representing details of an offer.

    Attributes:
    - offer (ForeignKey): References the associated offer.
    - title (CharField): Title of the offer detail.
    - revisions (IntegerField): Number of revisions allowed.
    - delivery_time_in_days (IntegerField): Estimated delivery time in days.
    - price (DecimalField): Price for the offer details.
    - features (JSONField): List of features included in the offer.
    - offer_type (CharField): Category of the offer ('basic', 'standard', or 'premium').

    Choices:
    - OFFER_DETAIL_CATEGORIES: Defines available offer categories.

    Methods:
    - __str__(): Returns the title of the offer detail as a string representation.
    """
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    OFFER_DETAIL_CATEGORIES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]
    title = models.CharField(max_length=255, default="detail titel")
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=255, choices=OFFER_DETAIL_CATEGORIES, default="standard")

    def __str__(self):
        return f"{self.title}"