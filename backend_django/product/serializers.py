from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
            "category"
        )


class MyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "category",
            "name",
            "slug",
            "description",
            "price",
            "image",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products"
        )

class MyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )