from django.urls import reverse
from rest_framework.test import APITestCase
from .functions import *


class OrderFunctionalityCheck(APITestCase):
    
    
    def setUp(self):
        return super().setUp()
    
    
    def test_create_order(self):
        
        url = reverse('orders')
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, fromat='json')