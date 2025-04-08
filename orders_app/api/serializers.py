from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetails


class OrderSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    revisions = serializers.SerializerMethodField()
    delivery_time_in_days = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    offer_type = serializers.SerializerMethodField()

    def get_revisions(self, obj):
        return obj.offerdetails.revisions

    def get_delivery_time_in_days(self, obj):
        return obj.offerdetails.delivery_time_in_days

    def get_price(self, obj):
        return obj.offerdetails.price

    def get_features(self, obj):
        return obj.offerdetails.features

    def get_offer_type(self, obj):
        return obj.offerdetails.offer_type

    def get_title(self, obj):
        return obj.offerdetails.offer.title

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context['request']
        offer_detail_id = validated_data['offer_detail_id']

        try:
            detail = OfferDetails.objects.get(id=offer_detail_id)
        except OfferDetails.DoesNotExist:
            raise serializers.ValidationError("OfferDetail wurde nicht gefunden.")

        return Order.objects.create(
            offerdetails=detail,
            customer_user=request.user,
            business_user=detail.offer.user,
            status="in_progress"
        )