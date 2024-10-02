from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        
class UserProdileUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'role', 'contact_number', 'street_address', 'city', 'postal_code','house_holding_number', 'profile_image']