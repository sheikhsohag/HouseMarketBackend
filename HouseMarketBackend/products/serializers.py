from rest_framework import serializers
from .models import Products, Category
from Accounts.models import User

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'category_slug']
