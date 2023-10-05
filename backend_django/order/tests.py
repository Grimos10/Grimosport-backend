from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Order, OrderItem
from product.models import Product, Category
import stripe
from django.conf import settings


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


class CheckoutTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.category1 = Category.objects.create(name='Summer', slug='summer')
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.0, category=self.category1)
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.0, category=self.category1)
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user=self.user)
        

    def test_checkout_with_valid_data(self):
        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        stripe.api_key = 'pk_test_51NsA1rBpXEnKYKYFHfPEReeMx6HdpuhzYvhjNsPrHEYOPKwt6qrJaJjQKkH1ueQdrm2tgjjdd3nv7JNRvnu5TkPn00BIvV2xTg'
        card = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': 12,
                'exp_year': 2023,
                'cvc': '123'
            }
        )
        url = '/api/v1/checkout/'
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'address': 'Testaddress',
            'zipcode': '123456',
            'place': 'Testplace',
            'phone': '123456789',
            'items': [
                {
                    'product': product1.id,
                    'quantity': 2,
                    'price': 10
                },
                {
                    'product': product2.id,
                    'quantity': 1,
                    'price': 20
                }
            ],
            'stripe_token': card.id,
        }
        print(data)
        response = self.client.post(url, data, headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_checkout_with_invalid_data(self):
        url = '/api/v1/checkout/'
        data = {
            'items': [
                {
                    'product': 1,
                    'quantity': 2,
                },
                {
                    'product': 2,
                    'quantity': 1
                }
            ],
            'stripe_token': 'tok_invalid'
        }
        response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
