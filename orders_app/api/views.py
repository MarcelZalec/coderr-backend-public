from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from orders_app.models import Order
from offers_app.models import OfferDetails, Offer
from profile_app.models import UserProfile
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_app.api.permissions import IsOwnerOrAdmin
from .permissions import *
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CompletedOrderCount(APIView):
    permission_classes = [ViewCounts]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, business_user_id):
        if not UserProfile.objects.filter(id = business_user_id):
            return Response({"error": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=status.HTTP_404_NOT_FOUND)
        try:
            completed_order_count = Order.objects.filter(business_user = business_user_id, status='completed').count()
            print(f"das ist der Count === {completed_order_count}")
            return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": f"Ein Fehler ist aufgetreten: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderCountAPIView(APIView):
    permission_classes = [ViewCounts]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, business_user_id):
        try:
            user = UserProfile.objects.get(user__id = business_user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.type != 'business':
            return Response({"error": "Kein Business-User."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count = Order.objects.filter(business_user = business_user_id, status="in_progress").count()
        return Response({'order_count':order_count}, status=status.HTTP_200_OK)


class OrderViewSet(APIView):
    permission_classes=[OrderPermission]
    authentication_classes = [TokenAuthentication]
    pagination_class = None
    
    
    def get(self, request, pk=None):
        if request.user.id == None:
            return Response({"error":"Benutzer ist nicht authentifiziert."},status=status.HTTP_401_UNAUTHORIZED)
        if pk:
            order = get_object_or_404(Order, pk=pk)
            if order.customer_user != request.user and order.business_user != request.user:
                return Response({'error': 'Keine Berechtigung für diese Bestellung.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            orders = Order.objects.filter(
                Q(customer_user=request.user) | Q(business_user=request.user)
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        """
        Creates a new order for the authenticated user.

        Parameters:
        request (Request): The request sent by the client.

        Returns:
        Response: A JSON response containing the serialized order data. If the user is not a customer, 
                returns a 403 error response. If neither offer_id nor offer_detail_id is provided, 
                returns a 400 error response. If the offer or offer_detail is not found, returns a 404 
                error response. If the offer's user is not the business user, returns a 400 error response.

        Notes:
        - The authenticated user must be a customer.
        - The request body must contain either 'offer_id' or 'offer_detail_id'.
        - If the request body contains 'offer_detail_id', the offer's details are used.
        - If the request body contains 'offer_id', the offer's details must be provided in the request 
        body.
        """
        data = request.data

        offer_id = data.get("offer_id")
        offer_detail_id = data.get("offer_detail_id")
        
        if not UserProfile.objects.filter(user = request.user.id):
            return Response({"error":"Benutzer ist nicht authentifiziert."},status=status.HTTP_401_UNAUTHORIZED)

        if not offer_id and not offer_detail_id:
            return Response({'error': 'Ein Angebot oder OfferDetail muss angegeben werden.'}, status=status.HTTP_400_BAD_REQUEST)

        if offer_detail_id:
            offer_detail = get_object_or_404(OfferDetails, pk=offer_detail_id)
            offer_id = offer_detail.offer.id
            revisions = offer_detail.revisions
            delivery_time_in_days = offer_detail.delivery_time_in_days
            price = offer_detail.price
            features = offer_detail.features
            offer_type = offer_detail.offer_type

        offer = get_object_or_404(Offer, pk=offer_id)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer.user,
            title=data.get("title", offer.title),
            revisions=data.get("revisions", revisions),
            delivery_time_in_days=data.get("delivery_time_in_days", delivery_time_in_days),
            price=data.get("price", price),
            features=data.get("features", features),
            offer_type=data.get("offer_type", offer_type),
            status="in_progress",
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def patch(self, request, pk):
        """
        Partially updates an existing order.

        Updates the status of an order. Only the `status` field can be updated.

        Parameters:
        pk (int): The id of the order to be updated.
        request (Request): A request object containing the new status in the request body.

        Returns:
        Response: A response object containing the updated order data with status 200.

        If the user is not the customer or the business user of the order, a 403 response is returned.

        If the request body does not contain a valid status, a 400 response is returned.
        """
        order = get_object_or_404(Order, pk=pk)
        
        if not UserProfile.objects.filter(user = request.user.id):
            return Response({"error":"Benutzer ist nicht authentifiziert."},status=status.HTTP_401_UNAUTHORIZED)

        if order.customer_user != request.user and order.business_user != request.user:
            return Response({'error': 'Keine Berechtigung für diese Bestellung.'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get("status")
        if not new_status or new_status not in dict(Order.ORDER_STATUS).keys():
            return Response(
                {'error': 'Ungültiger oder fehlender Status. Gültige Werte sind: ' + ', '.join(dict(Order.ORDER_STATUS).keys())},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)