from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .functions import *


class OrderFunctionalityCheck(APITestCase):
    
    
    def setUp(self):
        create_and_login_test_user(self)
        create_test_offer(self)
        create_test_offerdetails(self)
    
    
    def test_create_order(self):
        
        url = reverse('order-list-create')
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, fromat='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)