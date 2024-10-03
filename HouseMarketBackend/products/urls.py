
from django.urls import path, include
from .views import ProductApiView,  CategoryApiView

from products import views



urlpatterns = [
    path('products/', ProductApiView.as_view(), name = 'products'),
    path('product/<str:pk>/', ProductApiView.as_view(), name = 'product'),
    
    path('product/category/<str:pk>/', CategoryApiView.as_view(), name='create_category'),
    path('product/category/', CategoryApiView.as_view(), name='create_category'),
]
