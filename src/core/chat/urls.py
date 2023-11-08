from django.urls import path
from .views import TestAPIView, index, room

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='chat-test'),
    path('', index, name='chat-home'),
    path('<str:room_name>/', room, name='chat-room'),
]