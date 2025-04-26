from rest_framework import serializers
from profile_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
        """
    Serializer for handling UserProfile instances.

    Meta:
    - model: UserProfile.
    - fields: '__all__' (Includes all fields from the UserProfile model).

    Description:
    - This serializer is used to serialize and deserialize user profile data.
    - It provides full access to all attributes of a UserProfile instance.

    Usage:
    - Used in API views to handle user profile-related requests.
    """
        class Meta:
                model = UserProfile
                fields = "__all__"


class BusinessUserSerializer(serializers.ModelSerializer):
        """
    Serializer for business user profiles.

    Meta:
    - model: UserProfile.
    - fields: Includes attributes relevant for business users.

    Description:
    - This serializer specifically handles business user profiles.
    - Provides access to details like location, contact information, and working hours.

    Fields:
    - user: Associated user instance.
    - username: Business username.
    - first_name, last_name: Business user's name.
    - file: Uploaded profile-related files.
    - location: Business location.
    - tel: Business contact number.
    - description: Business description.
    - working_hours: Operational hours.
    - type: Defines user type ('business' or other).
    """
        class Meta:
                model = UserProfile
                fields = [
                        'user', 'username', 'first_name', 'last_name', 'file',
                        'location', 'tel', 'description', 'working_hours', 'type'
                ]


class CustomerUserSerializer(serializers.ModelSerializer):
        """
    Serializer for customer user profiles.

    Meta:
    - model: UserProfile.
    - fields: Includes attributes relevant for customer users.

    Description:
    - This serializer handles customer user profiles.
    - Provides access to essential user details but excludes business-related fields.

    Fields:
    - user: Associated user instance.
    - username: Customer's username.
    - first_name, last_name: Customer's name.
    - file: Uploaded profile-related files.
    - type: Defines user type ('customer' or other).
    """
        class Meta:
                model = UserProfile
                fields = [
                        'user', 'username', 'first_name', 'last_name', 'file','type'
                ]