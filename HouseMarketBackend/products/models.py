from django.db import models
from Accounts.models import User


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User model
    name = models.CharField(max_length=255)  # Product name
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
        return f"{self.name} by {self.user.email}"  # Display product name with associated user

    class Meta:
        ordering = ['-created_at']  # Order by newest first
