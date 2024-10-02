
from django.urls import path, include
from .views import getProducts, CategoryApiView

from products import views



urlpatterns = [
    path('products/', views.getProducts, name='getproducts'),
    path('product/<str:pk>', views.getProduct, name='getproduct'),
    path('profuct/category/create/', CategoryApiView.as_view(), name='create_category'),
]
