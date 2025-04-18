from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .functions import *

class ProfileFunctionalityCheck(APITestCase):
    
    def setUp(self):
        create_and_login_test_user(self)
    
    
    def test_get_profile(self):
        url = reverse('profile-detail', kwargs={'user': self.user.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client.logout()
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_not_found(self):
        newId = 5
        url = reverse('profile-detail', kwargs={'user': newId})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_getBusiness_user_list(self):
        url = reverse('profiles-business-list')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)