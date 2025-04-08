from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):

    # 2 felder ergänzt:
    repeated_password = serializers.CharField(write_only=True)

    type = serializers.ChoiceField(
        choices=UserProfile.USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    # validation - wird automatisch ausgeführt wenn es so heißt

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match!'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'This email is already in use!'})

        return data

    # save() nicht überschreiben! - lieber create und update haben
    # def save(self):

    def create(self, validated_data):
   
        # inhalt sichern
        user_type = validated_data['type']

        # raus!
        validated_data.pop('repeated_password')
        validated_data.pop('type')

        # keys "entpacken" und erstellen
        user = User.objects.create_user(**validated_data)

        # user UND user_type zurückgeben, dann wird in views gespeichert
        return user, user_type


class ResetPasswordRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    Validates that a valid email is provided.
    """

    email = serializers.EmailField(required=True)