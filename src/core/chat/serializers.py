from rest_framework.serializers import ModelSerializer

from chat.models import Room
from auth_core.models import CustomUser

class RoomCreateSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_name']


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'room_name', 'owner_id', 'room_status']


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']
