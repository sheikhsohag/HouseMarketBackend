from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Products, Category
# Create your views here.
from .serializers import ProductsSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status


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




