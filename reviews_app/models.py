from django.db import models
from django.contrib.auth.models import User


class Reviews(models.Model):
    """
    Model representing user reviews for businesses.

    Attributes:
    - reviewer (ForeignKey): References the user submitting the review.
    - business_user (ForeignKey): References the business receiving the review.
    - rating (IntegerField): Stores the rating given by the reviewer.
    - description (TextField): Review description provided by the user.
    - created_at (DateTimeField): Timestamp for when the review was created.
    - updated_at (DateTimeField): Timestamp for when the review was last updated.

    Constraints:
    - Ensures a unique review per reviewer-business user pair.

    Meta:
    - Unique constraint on ('reviewer', 'business_user') to prevent duplicate reviews.

    Methods:
    - __str__(): Returns a formatted string representation of the review.
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reviewer', 'business_user'],
                name='unique_review_per_user_pair'
            )
        ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_gotten")
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)