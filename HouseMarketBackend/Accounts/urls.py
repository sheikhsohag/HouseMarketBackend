from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views
from .views import SignUpView

urlpatterns = [
     path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
     path('home/', views.HomeView.as_view(), name ='home'),
     path('logout/', views.LogoutView.as_view(), name ='logout'),
     path('signup/', SignUpView.as_view(), name='signup'),
]