from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Products
# Create your views here.
from .serializers import ProductsSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

@api_view(['GET'])
def getRoutes(request):
    return Response('Hello anees')


@api_view(['GET'])
def getProducts(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Products.objects.get(id=pk)
    serializer = ProductsSerializer(product, many=False)
    return Response(serializer.data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token

class MYTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(['GET'])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

