from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from orders_app.models import Order
from profile_app.models import UserProfile
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_app.api.permissions import setStandartPermission, IsOwnerOrAdmin


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('created_at')
    permission_classes=[setStandartPermission]
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)


class CompletedOrderCount(APIView):
    permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, business_user_id):
        try:
            completed_order_count = Order.objects.filter(business_user = business_user_id, status='completed').count()
            return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'error': f'Ein Fehler ist aufgetreten: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderCountAPIView(APIView):
    permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, business_user_id):
        try:
            user = UserProfile.objects.get(user__id = business_user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile wurde nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.type != 'business':
            return Response({"error": "Kein Business-User."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count = Order.objects.filter(business_user = business_user_id, status="in_progress").count()
        return Response({'order_count':order_count}, status=status.HTTP_200_OK)