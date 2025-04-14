from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reviews_app.models import Reviews
from profile_app.models import UserProfile
from offers_app.models import Offer
from django.db.models import Avg
from rest_framework.permissions import AllowAny

class BaseInfoView(APIView):
    permission_classes = [AllowAny]
    """
    API endpoint that provides basic platform statistics, including the number of reviews,
    average rating, number of business profiles, and number of offers.
    """
    def get(self, request, *args, **kwargs):
        
        review_count = Reviews.objects.count()
        average_rating = Reviews.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        business_profile_count = UserProfile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        
        average_rating = round(average_rating, 1) if average_rating is not None else 0.0

        
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        return Response(data, status=status.HTTP_200_OK)