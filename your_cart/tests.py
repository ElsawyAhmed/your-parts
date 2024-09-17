from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.token_url = '/api/v1/auth/token/'
        self.refresh_url = '/api/v1/auth/token/refresh/'

    def test_obtain_jwt_token(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_jwt_token(self):
        # Get the refresh token
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass123'})
        refresh_token = response.data['refresh']

        # Use the refresh token to get a new access token
        response = self.client.post(self.refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)