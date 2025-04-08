from rest_framework import serializers
from reviews_app.models import Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"


class ReviewsPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ["business_user", "rating", "description"]

    def validate(self, data):
        request = self.context['request']
        reviewer = request.user
        business_user = data.get('business_user')

        if Reviews.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError("Du kannst nur eine Bewertung pro Anbieter schreiben!")
        return data