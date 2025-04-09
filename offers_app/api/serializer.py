from rest_framework import serializers
from offers_app.models import Offer, OfferDetails
from django.db.models import Min
from profile_app.models import UserProfile


class OfferDetailURLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        exclude = ['offer']


class OffersListSerializer(serializers.ModelSerializer):

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
        # print(f"User ID == { UserProfile.objects.get(id)} und obj ID == {obj.user_id}")
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

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetails.objects.create(offer=instance, **detail_data)

        return instance


class SingleOfferListSerializer(serializers.ModelSerializer):

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
    
    class Meta:
        model = Offer
        fields = '__all__'
    
    def create(self, validated_data):
        return super().create(validated_data)