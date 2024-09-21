
from django.urls import path, include
from .views import GoogleLoginApi
from googleLogin import views



urlpatterns = [
   path('login/google/', GoogleLoginApi.as_view(), name="google-login")
]
