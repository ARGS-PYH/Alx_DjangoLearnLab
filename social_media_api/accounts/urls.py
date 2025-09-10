from django.urls import path
from .views import RegisterAPIView, ProfileAPIView, CustomObtainAuthToken
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'), 
    path('profile/', ProfileAPIView.as_view(), name='profile'),     
]
