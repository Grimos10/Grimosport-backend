import stripe
import json
import ast

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status, authentication, permissions 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer 

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    print(request.data)
    data = {}
    print(request.data['items'])
    for key, value in request.data.items():
        if key == 'items':
            print(value)
            print(type(value))
            item_list = []
            item_list = ast.literal_eval(value)
            data[key] = item_list
        else:
            data[key] = str(value) if value else None
    print(data)
    serializer = OrderSerializer(data=data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='EUR',
                description='Charge from Grimos',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


