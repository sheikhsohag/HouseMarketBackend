from django.contrib import admin
from .models import Products  # Import the Product model

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'price', 'stock', 'image']  
admin.site.register(Products, ProductsAdmin)
