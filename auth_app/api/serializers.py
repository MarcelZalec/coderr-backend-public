from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
    - repeated_password (CharField): Ensures the password confirmation.
    - type (ChoiceField): Defines the type of user (business/customer).

    Meta:
    - model: User model.
    - fields: ['username', 'email', 'password', 'repeated_password', 'type'].

    Methods:
    - validate(data): Checks password match and uniqueness of the email.
    - create(validated_data): Creates a new user and assigns a type.

    Raises:
    - serializers.ValidationError: If passwords do not match or email exists.
    """

    repeated_password = serializers.CharField(write_only=True)


    type = serializers.ChoiceField(
        choices=UserProfile.USER_TYPES, required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']


    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match!'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'This email is already in use!'})

        return data


    def create(self, validated_data):
   

        user_type = validated_data['type']


        validated_data.pop('repeated_password')
        validated_data.pop('type')


        user = User.objects.create_user(**validated_data)


        return user, user_type


class ResetPasswordRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    Validates that a valid email is provided.
    """

    email = serializers.EmailField(required=True)