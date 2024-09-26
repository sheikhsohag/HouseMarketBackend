from django.urls import include, path
from .views import activation_redirect
from djoser.views import TokenCreateView, TokenDestroyView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<uidb64>/<token>/', activation_redirect, name='activation_redirect'),
]


