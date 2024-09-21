
from django.urls import path, include
from .views import getProducts
from products import views



urlpatterns = [
    path('products/', views.getProducts, name='getproducts'),
    path('product/<str:pk>', views.getProduct, name='getproduct'),
   
]
