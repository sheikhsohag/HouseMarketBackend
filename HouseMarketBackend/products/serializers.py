from rest_framework import serializers
from .models import Products, Category
from Accounts.models import User
from .models import Cart, CartItem, Order

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'category_slug']




class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'price_at_time']
    def create(self, validated_data):
        
        return CartItem

class CartSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), many=True)

    class Meta:
        model = Cart
        fields = ['user', 'items', 'total_amount']

    def create(self, validated_data):
        items = validated_data.pop('items')  # Extract the items data
        cart = Cart.objects.create(**validated_data)  # Create the cart
        cart.items.set(items)  # Associate the items (products) with the cart
        return cart


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_number', 'status', 'total_price', 'created_at']

