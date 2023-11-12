from django.urls import path
from chat.views import TestAPIView, RoomAPIView

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='chat-test'),
    path('room/', RoomAPIView.as_view(), name='chat-room'),
]