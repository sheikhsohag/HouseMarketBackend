from django.db import models
from Accounts.models import User
from django.db import models
from django.utils.text import slugify
import random
import string


class Products(models.Model):
    # give user id...during form control 
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)  # Reference to User model
    product_name = models.CharField(max_length=255)  # Product name
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    discountPrice = models.FloatField(default=0, null=True, blank=True)
    description = models.TextField()  # Detailed description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    stock = models.IntegerField(default=0)  # Available stock quantity
    rating = models.FloatField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)  # Date when product was added
    updated_at = models.DateTimeField(auto_now=True)  # Date when product was last updated
   

    def __str__(self):
        return f"{self.product_name} by {self.user.email}"  # Display product name with associated user

    class Meta:
        ordering = ['-created_at']  # Order by newest first




class Category(models.Model):
    category = models.CharField(max_length=155, unique=True)
    category_slug = models.SlugField(max_length=155, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(self.category)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category
    
# cart started
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Products)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"


ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),           
    ('processing', 'Processing'),     
    ('shipped', 'Shipped'),           
    ('delivered', 'Delivered'),     
    ('cancelled', 'Cancelled'),        
]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super(Order, self).save(*args, **kwargs)

    def generate_order_number(self):
        """Generate a unique order number."""
        order_number = 'ORD' + ''.join(random.choices(string.digits, k=10))
        while Order.objects.filter(order_number=order_number).exists():
            order_number = 'ORD' + ''.join(random.choices(string.digits, k=10))
        return order_number

    def __str__(self):
        return self.order_number




