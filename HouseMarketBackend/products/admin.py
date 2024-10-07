from django.contrib import admin
from .models import Products, Category  # Import the Product model
from .models import Cart, CartItem, Order

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','product_name', 'user', 'price', 'stock', 'image']  
admin.site.register(Products, ProductsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category', 'category_slug']
admin.site.register(Category, CategoryAdmin)






class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_items', 'total_amount', 'created_at')

    # Custom method to display items
    def get_items(self, obj):
        return ", ".join([str(item) for item in obj.items.all()])

    get_items.short_description = 'Items'  

    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_number', 'user__username')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
