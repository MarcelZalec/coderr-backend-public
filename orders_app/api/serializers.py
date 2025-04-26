from rest_framework import serializers
from orders_app.models import Order

        
class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for managing Order objects.

    Meta:
    - model: Order.
    - fields: '__all__' (Includes all fields from the Order model).
    - read_only_fields: Specifies 'id', 'created_at', and 'updated_at' as read-only.

    Description:
    - This serializer is used to serialize and deserialize order data.
    - The 'id', 'created_at', and 'updated_at' fields are marked as read-only to prevent modifications.

    Usage:
    - Used in API views to handle order-related requests.
    - Ensures proper data validation when processing order instances.
    """

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')