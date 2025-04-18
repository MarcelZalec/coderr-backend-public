from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class ReviewsTests(APITestCase):

    def setUp(self):
        url = reverse('registration')

        data_busi = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business"
        }

        data_cust = {
            "username": "exampleUsername2",
            "email": "example2@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        response1 = self.client.post(url, data_busi, format="json")
        response2 = self.client.post(url, data_cust, format="json")

        # variablen in self speichern, dann sind sie global verfügbar
        self.token1 = response1.data['token']
        self.user_id1 = response1.data['user_id']
        self.token2 = response2.data['token']
        self.user_id2 = response2.data['user_id']

    def test_post_review(self):
        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')

        data = {
            "business_user": self.user_id1,
            "rating": 4,
            "description": "Alles war toll!"
        }

        url = reverse('reviews-list')

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_keys = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]

        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_patch_review(self):
        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')

        data = {
            "business_user": self.user_id1,
            "rating": 4,
            "description": "Alles war toll!"
        }

        url = reverse('reviews-list')

        response = self.client.post(url, data, format="json")
        review_id = response.data["id"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('reviews-detail', kwargs={"pk": review_id})

        data = {
            "rating": 1,
            "description": "schlimm!"
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_keys = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]

        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_get_reviews_no_auth(self):
        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {''}')

        url = reverse('reviews-list')

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)