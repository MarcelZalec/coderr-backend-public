from rest_framework import serializers, status
from offers_app.models import Offer, OfferDetails
from django.db.models import Min
from profile_app.models import UserProfile
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class OfferDetailURLSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for generating URLs for OfferDetails.

    Meta:
    - model: OfferDetails.
    - fields: ['id', 'url'].
    """
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetails, excluding the related offer field.

    Meta:
    - model: OfferDetails.
    - exclude: ['offer'].
    """
    class Meta:
        model = OfferDetails
        exclude = ['offer']


class OffersListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing offers with detailed information.

    Attributes:
    - details: Related OfferDetails serialized as URLs.
    - min_price: Minimum price calculation using SerializerMethodField.
    - min_delivery_time: Minimum delivery time calculation.
    - user_details: User profile details.

    Meta:
    - model: Offer.
    - fields: Contains offer attributes.

    Methods:
    - get_min_price(obj): Returns the minimum price among offer details.
    - get_min_delivery_time(obj): Returns the minimum delivery time.
    - get_user_details(obj): Returns user profile information.
    """

    details = OfferDetailURLSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'details', 'image',
                  'description', 'created_at', 'updated_at',
                  'min_price', 'min_delivery_time',
                  'user_details']

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_time=Min('delivery_time_in_days'))['min_time']

    def get_user_details(self, obj):
        try:
            user = UserProfile.objects.get(user_id=obj.user_id)
        except UserProfile.DoesNotExist:
            return {}

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing offer data.

    Attributes:
    - details: Nested OfferDetailsSerializer.

    Meta:
    - model: Offer.
    - fields: ["id", "title", "image", "description", "details"].

    Methods:
    - create(validated_data): Creates a new offer along with offer details.
    - update(instance, validated_data): Updates an existing offer with new details.
    """

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        if len(details_data) != 3:
            raise NotFound("Es müssen genau 3 Details vorhanden sein")
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        d_type = validated_data.pop('offer_type', None)
        
        print(d_type)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if len(details_data) != 3:
            raise NotFound("Es müssen genau 3 Details vorhanden sein")
        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetails.objects.create(offer=instance, **detail_data)

        return instance


class SingleOfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving details of a single offer.

    Attributes:
    - details: Nested OfferDetailURLSerializer.
    - min_price: Minimum price calculation.
    - min_delivery_time: Minimum delivery time calculation.

    Meta:
    - model: Offer.
    - fields: Contains attributes relevant to a single offer.

    Methods:
    - get_min_price(obj): Returns the minimum price of offer details.
    - get_min_delivery_time(obj): Returns the minimum delivery time of offer details.
    """

    details = OfferDetailURLSerializer(many=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description",
                  "details", "created_at", "updated_at",
                  'min_price', 'min_delivery_time']

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_time=Min('delivery_time_in_days'))['min_time']



class GetOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for fetching offer details.

    Attributes:
    - details: Nested OfferDetailSerializer.

    Meta:
    - model: Offer.
    - exclude: ['created_at', 'updated_at', 'user'].

    Methods:
    - create(validated_data): Creates an offer along with details.
    """

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        exclude = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer


class OffersXXSerializer(serializers.ModelSerializer):
    """
    Generic serializer for Offer model with all fields included.

    Meta:
    - model: Offer.
    - fields: '__all__'.

    Methods:
    - create(validated_data): Calls the parent method to create an instance.
    """
    
    class Meta:
        model = Offer
        fields = '__all__'
    
    def create(self, validated_data):
        return super().create(validated_data)