# views.py
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProdileUpdateSerializers
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser

def activation_redirect(request, uidb64, token):
    try:
        frontend_url = f"http://localhost:5173/activate/{uidb64}/{token}/"
        return redirect(frontend_url)
    except Exception as e:
        return HttpResponse("Activation link is invalid.", status=400)
    
# user registration and deleted handle by djoser..

class UserProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        pk = request.user.id
        
        instance, created = User.objects.get_or_create(pk=pk)
        serializer = UserProdileUpdateSerializers(instance, data=request.data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User Profile updated successfully!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
