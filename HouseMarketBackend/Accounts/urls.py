from django.urls import include, path
from .views import activation_redirect
from djoser.views import TokenCreateView, TokenDestroyView
from .views import UserProfileApiView


urlpatterns = [
    # djoser package properties
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<uidb64>/<token>/', activation_redirect, name='activation_redirect'),
    # my create or override properties
    path('profile/update/', UserProfileApiView.as_view(), name='prodile_update'),
]


