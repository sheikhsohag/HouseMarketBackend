
from django.urls import path, include
from .views import ProductApiView,  CategoryApiView

from products import views
from .views import CartApiView, CartItemAPIView



urlpatterns = [
    path('products/', ProductApiView.as_view(), name = 'products'),
    path('product/<str:pk>/', ProductApiView.as_view(), name = 'product'),
    
    path('product/category/<str:pk>/', CategoryApiView.as_view(), name='create_category'),
    path('product/category/', CategoryApiView.as_view(), name='create_category'),

    # cart releted

    path('cart/', CartApiView.as_view(), name='cart-detail'),
    path('cart/items/', CartItemAPIView.as_view(), name='cart-items'),
    path('cart/item/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),

]
