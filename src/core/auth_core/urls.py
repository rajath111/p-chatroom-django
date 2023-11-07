from django.urls import path
from auth_core.views import UserLoginAPIView, UserRegisterationAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('register/', UserRegisterationAPIView.as_view(), name='user-registeration'),
]