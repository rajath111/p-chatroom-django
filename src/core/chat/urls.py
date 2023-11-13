from django.urls import path
from chat.views import TestAPIView, RoomAPIView, RoomDetailAPIView, RoomMembershipDetailAPIView, RoomMembershipApiView

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='chat-test'),
    path('room/', RoomAPIView.as_view(), name='chat-room'),
    path('room/<str:room_id>/', RoomDetailAPIView.as_view(), name='chat-room-detail'),
    path('members/', RoomMembershipApiView.as_view(), name='member'),
    path('members/<str:room_id>/', RoomMembershipDetailAPIView.as_view(), name='member-detail'),
]