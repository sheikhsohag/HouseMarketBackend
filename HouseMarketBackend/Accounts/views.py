from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer
from .models import User


class SignUpView(APIView):
    def post(self, request):
        # Pass both data and files to the serializer
        serializer = UserSerializer(data=request.data)

        # Check if the request data is valid
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class HomeView(APIView):     
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
       return Response(content)


class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          refresh_token = request.data["refresh_token"]
          token = RefreshToken(refresh_token)
          try:

               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)