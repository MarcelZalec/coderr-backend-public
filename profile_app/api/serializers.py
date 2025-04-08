from rest_framework import serializers
from profile_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = "__all__"


class BusinessUserSerializer(serializers.ModelSerializer):
        class Meta:
                model = UserProfile
                fields = [
                        'user', 'username', 'first_name', 'last_name', 'file',
                        'location', 'tel', 'description', 'working_hours', 'type'
                ]


class CustomerUserSerializer(serializers.ModelSerializer):
        class Meta:
                model = UserProfile
                fields = [
                        'user', 'username', 'first_name', 'last_name', 'file','type'
                ]