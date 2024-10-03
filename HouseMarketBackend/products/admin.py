from django.contrib import admin
from .models import Products, Category  # Import the Product model

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','product_name', 'user', 'price', 'stock', 'image']  
admin.site.register(Products, ProductsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category', 'category_slug']
admin.site.register(Category, CategoryAdmin)