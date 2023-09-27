from django.http import Http404
from django.db.models import Q, Count
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions, status


from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, MyProductSerializer, MyCategorySerializer

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
    
class SetProduct(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        img = request.FILES['image']
        product = Product.objects.create(
            category_id=request.data.get('category'),
            name=request.data.get('name'),
            slug=request.data.get('slug'),
            description=request.data.get('description'),
            price=request.data.get('price'),
            image=img
        )
        if product:
            product.save()
            return Response({"message": "Product created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Product not created"}, status=status.HTTP_400_BAD_REQUEST)
                          
        #serializer = MyProductSerializer(data=request.data)
        #print(request.data)
       #print("SPAZIO")
       # print(serializer)
      #  if serializer.is_valid():
        #    serializer.save()
     #       return Response(serializer.data, status=status.HTTP_201_CREATED)
      #  else:
      #      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCategories(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = MyCategorySerializer(categories, many=True)
        return Response(serializer.data)
    

class ProductStats(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        cursor = connection.cursor()
        cursor.execute('''
                    SELECT p.id, p.name, SUM(op.quantity) AS quantity_orders_product, count(o.id) AS quantity_orders
                    FROM product_product p
                    LEFT JOIN order_orderitem op ON op.product_id = p.id
                    LEFT JOIN order_order o ON o.id = op.order_id
                    GROUP BY p.id, p.name
                    ORDER BY quantity_orders_product DESC;''')
        result = cursor.fetchall()
        #make result to dict
        i = 0
        for r in result:
            product = Product.objects.get(id=r[0])
            serializer = ProductSerializer(product)
            result[i] = {
                'id_product': r[0],
                'name_product': r[1],
                'quantity_orders_product': r[2],
                'quantity_orders': r[3],
                'price_product': serializer.data['price'],
                'absolute_url_product': serializer.data['get_absolute_url'],
            }
            i += 1
        return Response(result)