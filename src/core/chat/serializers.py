from rest_framework.serializers import ModelSerializer, IntegerField

from chat.models import Room, RoomMembership
from auth_core.models import CustomUser

class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']


class RoomCreateSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_name']


class RoomSerializer(ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    class Meta:
        model = Room
        fields = ['id', 'room_name', 'owner_id', 'room_status', 'owner']
        depth = 1


class RoomMembershipSerializer(ModelSerializer):
    room_id = IntegerField(read_only=False)
    user_id = IntegerField(read_only=False)

    class Meta:
        model = RoomMembership
        fields = ['room_id', 'user_id']

