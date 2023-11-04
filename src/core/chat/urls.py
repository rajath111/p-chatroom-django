from django.urls import path
from .views import test, index, room

urlpatterns = [
    path('test', test, name='chat-test'),
    path('', index, name='chat-home'),
    path('<str:room_name>/', room, name='chat-room'),
]