from django.http import Http404
from django.db.models import Q, Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions


from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

from order.models import Order, OrderItem
from order.serializers import OrderSerializer, MyOrderSerializer

class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class MoreBuyedProductList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request):
        orders = Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.filter(order__in=orders.values_list('id', flat=True))
        products = Product.objects.filter(id__in=order_items.values_list('product', flat=True)).annotate(buyed=Count('id')).order_by('-buyed')[0:4]
        serializer = ProductSerializer(products, many=True)
        summer = 0
        winter = 0
        for i in serializer.data:
            if i.get('category') == 1:
                summer += 1
            else:
                winter += 1
        if summer == 0 and winter == 0:
            return []
        if summer > winter:
            return self.get_more_buyed_summer_products(request)
        else:
            return self.get_more_buyed_winter_products(request)
        
    def get_more_buyed_summer_products(self, request):
        products = Product.objects.filter(category=1)[0:4]
        return products
    
    def get_more_buyed_winter_products(self, request):
        products = Product.objects.filter(category=2)[0:4]
        return products
    
    def get(self, request, format=None):
        products = self.get_object(request)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products': []}) 
    