
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse


class TestSum(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get-sum')  # Assume the URL is named 'book-list-create'

    def test_sum(self):
        data = {"numbers": [1,2,3]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['sum'], 6)
