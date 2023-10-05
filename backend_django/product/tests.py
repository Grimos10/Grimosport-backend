from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, MyProductSerializer, MyCategorySerializer
from order.models import Order, OrderItem
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Test case for LatestProductList
class LatestProductListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/latest-products/'
        self.category1 = Category.objects.create(name='Summer', slug='summer')
        self.category2 = Category.objects.create(name='Winter', slug='winter')
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.0, category=self.category1, slug='product-1')
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.0, category=self.category1, slug='product-2')
        self.product3 = Product.objects.create(name='Product 3', description='Description 3', price=30.0, category=self.category2, slug='product-3')
        self.product4 = Product.objects.create(name='Product 4', description='Description 4', price=40.0, category=self.category2, slug='product-4')

    def test_latest_product_list(self):
        response = self.client.get(self.url)
        products = Product.objects.all().order_by('-id')[:4]
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test case for MoreBuyedProductList
class MoreBuyedProductListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/more-buyed-products/'
        self.user = User.objects.create(username='test', password='test')
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.category1 = Category.objects.create(name='Summer', slug='summer')
        self.category2 = Category.objects.create(name='Winter', slug='winter')
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.0, category=self.category1)
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.0, category=self.category1)
        self.product3 = Product.objects.create(name='Product 3', description='Description 3', price=30.0, category=self.category2)
        self.product4 = Product.objects.create(name='Product 4', description='Description 4', price=40.0, category=self.category2)
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_more_buyed_product_list(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product1, price=self.product1.price, quantity=1)
        OrderItem.objects.create(order=order, product=self.product2, price=self.product2.price, quantity=1)
        OrderItem.objects.create(order=order, product=self.product3, price=self.product3.price, quantity=1)
        OrderItem.objects.create(order=order, product=self.product4, price=self.product4.price, quantity=1)
        response = self.client.get(self.url, headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test case for ProductDetail
class ProductDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Summer', slug='summer')
        self.product = Product.objects.create(name='Product 1', slug='product-1', description='Description 1', price=10.0, category=self.category)
        self.url = '/api/v1/products/summer/product-1/'

    def test_product_detail(self):
        response = self.client.get(self.url)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test case for CategoryDetail
class CategoryDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Summer', slug='summer')
        self.url = '/api/v1/products/summer/'

    def test_category_detail(self):
        response = self.client.get(self.url)
        serializer = CategorySerializer(self.category)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test case for search
class SearchTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/products/search/'
        self.category1 = Category.objects.create(name='Summer', slug='summer')
        self.category2 = Category.objects.create(name='Winter', slug='winter')
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.0, category=self.category1, slug='product-1')
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.0, category=self.category1, slug='product-2')
        self.product3 = Product.objects.create(name='Product 3', description='Description 3', price=30.0, category=self.category2, slug='product-3')
        self.product4 = Product.objects.create(name='Product 4', description='Description 4', price=40.0, category=self.category2, slug='product-4')

    def test_search(self):
        response = self.client.post(self.url, {'query': 'Product'})
        products = Product.objects.filter(name__icontains='Product') | Product.objects.filter(description__icontains='Product')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Test case for SetProduct
class SetProductTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/add-product/'
        self.user = User.objects.create(username='test', password='test')
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.category = Category.objects.create(name='Summer', slug='summer')
        self.product = Product.objects.create(name='Product 1', slug='product-1', description='Description 1', price=10.0, category=self.category)

    def test_set_product(self):
        response = self.client.post(self.url, {'name': 'Product 2', 'slug': 'product-2', 'description': 'Description 2', 'price': 20.0, 'category': self.category.id}, headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# Test case for GetCategories
class GetCategoriesTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/get-categories/'
        self.category1 = Category.objects.create(name='Summer', slug='summer')
        self.category2 = Category.objects.create(name='Winter', slug='winter')

    def test_get_categories(self):
        response = self.client.get(self.url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)