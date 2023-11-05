from django.urls import re_path
from chat.consumers import ChatConsumer

ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', view=ChatConsumer.as_asgi(), name='chat-room-socket'),
]