from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class OrdersViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='test', password='test')
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_get_order_list(self):
        response = self.client.get('/api/v1/orders/', headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)