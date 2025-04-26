from rest_framework import serializers
from reviews_app.models import Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Reviews instances.

    Description:
    - This serializer provides full access to all attributes of a Reviews instance.
    - Used for retrieving and managing review data in API responses.

    Usage:
    - Typically used in API views to serialize review-related requests.
    """
    class Meta:
        model = Reviews
        fields = "__all__"


class ReviewsPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        """
    Serializer for creating new reviews.

    Meta:
    - model: Reviews.
    - fields: ['business_user', 'rating', 'description'] (Limits fields to necessary ones for posting a review).

    Methods:
    - validate(data): Ensures that a reviewer can only submit one review per business user.

    Raises:
    - serializers.ValidationError: If the reviewer has already reviewed the business user.

    Usage:
    - Used in API views to validate and process review submission requests.
    """
        model = Reviews
        fields = ["business_user", "rating", "description"]

    def validate(self, data):
        """
        Validates the review submission.

        Parameters:
        - data: The request data containing the review details.

        Returns:
        - Validated data if all checks pass.

        Raises:
        - ValidationError: If the reviewer has already submitted a review for the same business user
          and the request is not a PATCH update.
        """
        request = self.context['request']
        reviewer = request.user
        business_user = data.get('business_user')

        if Reviews.objects.filter(reviewer=reviewer, business_user=business_user).exists() and request.method != 'PATCH':
            raise serializers.ValidationError("Du kannst nur eine Bewertung pro Anbieter schreiben!")
        return data