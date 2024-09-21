from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'profile_image',
            'address', 'gender', 'role', 'password'
        ]



    def create(self, validated_data):
      
        password = validated_data.pop('password')

        # Create the user instance
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
