from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Products, Category, Cart, CartItem,Order
# Create your views here.
from .serializers import ProductsSerializer, CategorySerializer, CartItemSerializer, CartSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from .amount import recalculate_total_amount

class ProductApiView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk=None, *arg, **kwarg):
        if pk is None:
            product = Products.objects.all()
            serializer = ProductsSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            product = Products.objects.get(pk=pk)
            if product:
                serializer = ProductsSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message":"Such Product Does Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        
            
        except Products.DoesNotExist:
            return Response({"message":"Such Product does not contain"}, status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request, *arg, **kwarg):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Product successfully Created!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, *arg, **kwarg):
        instance = Products.objects.get(pk=pk)
        serializer = ProductsSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Product Successfully Updated!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *arg, **kwarg):
        if pk:
            instance = Products.objects.get(pk=pk)
            instance.delete()
            return Response({"message":"Product Deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"Product Id Required!"}, status=status.HTTP_404_NOT_FOUND)

    

class CategoryApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, *arg, **kwarg):
        if pk is None:
            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *arg, **kwarg):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, *arg, **kwarg):
        instance = Category.objects.get(pk=pk)
        serializer = CategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response({"error": "Category ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        


#started with  cart 

class CartApiView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        # Fetch the cart for the authenticated user
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"message": "Cart not found!"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the cart data
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        serializer = CartSerializer(cart, data=request.data, partial=True)
        
        if serializer.is_valid():
            new_items = request.data.get('items', [])  # Assuming 'items' is a list of product IDs

            if new_items:
                # Loop through the items and check if they already exist in the cart
                for product_id in new_items:
                    product = Products.objects.get(id=product_id)  # Get the product object by ID
                    

                    # Check if the product is already in the cart
                    if cart.items.filter(id=product.id).exists():
                        return Response({"message": f"Product {product_id} is already in the cart!"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # If product is not in the cart, add it
                    cart.items.add(product)


                    # when click added to cart then cartItem object create.. 
                    cartItemss = CartItem.objects.create(cart=cart, product=product, quantity=1, price_at_time=product.price)
                    cart.total_amount = cart.total_amount + product.price
                    cart.save()
                    return Response({"message": "Product added to Cart Successfully!"}, status=status.HTTP_201_CREATED)

            return Response({"message": "Product added to Cart Successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)

        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart.items.remove(product_id)  # assuming items is a ManyToManyField or ForeignKey
            cart.save()
            return Response({"message": "Product removed from Cart successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, reqeust, *arg, **kwarg):
        user = reqeust.user

        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response({"message":"Cart is Empty!"},status=status.HTTP_204_NO_CONTENT)
        cart.delete()
        return Response({"message": "Cart Remove Successfully!"}, status=status.HTTP_200_OK)
    



class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            cart_item = get_object_or_404(CartItem, id=pk)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            cart_items = CartItem.objects.all()
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
    def patch(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            recalculate_total_amount(cart_item.cart)
           
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk)
        product_id = cart_item.product.id
        cart = Cart.objects.get(user=request.user)
        

        print(product_id, cart, cart_item)
        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart.items.remove(product_id)  # assuming items is a ManyToManyField or ForeignKey
            cart.total_amount = cart.total_amount - cart_item.quantity * cart_item.price_at_time
            cart.save()
            cart_item.delete()
            return Response({"message": "Product removed from Cart successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request, pk=None):
        if pk:
            try:
                order = Order.objects.get(pk=pk, user=request.user)
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the authenticated user as the order owner
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            order.delete()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
