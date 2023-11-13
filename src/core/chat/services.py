from chat.models import Room, RoomMembership
from auth_core.models import CustomUser
from chat.serializers import RoomSerializer, RoomMembershipSerializer

class RoomService:
    def __init__(self) -> None:
        pass


    def create_room(self, room_name: str, user: CustomUser) -> Room:
        assert room_name, 'Room name can not be None'
        assert user, 'User can not be None'


        new_room = Room(room_name=room_name, owner_id=user.id, room_status='Closed')
        new_room.save()

        # Create room membership
        membership = RoomMembership(room_id=new_room.id, user_id=user.id)
        membership.save()

        return new_room


    def delete_room(self, room_id:str, user: CustomUser) -> bool:
        assert room_id, 'Room Id can not be None'
        assert user, 'User can not be None'

        try:
            room = Room.objects.get(id=room_id)
        except Exception as e:
            raise Exception('Room does not exists')

        assert room.owner_id == user.id, 'User is not the owner of group to delete group'
        room.delete()
        return True

    
    def get_room(self, room_id: str, user: CustomUser) -> Room:
        assert room_id, 'Room Id can not be None'
        assert user, 'User can not be None'

        try:
            room = Room.objects.get(id=room_id)
        except Exception as e:
            raise Exception('Room does not exists')

        assert room.owner_id == user.id, 'User is not the owner of group to delete group'
        return room


    def update_room(self, room_id: str, user: CustomUser, data) -> Room:
        assert room_id, 'Room Id can not be None'
        assert user, 'User can not be None'
        assert data, 'Data can not be None'
        print(data)
        try:
            room = Room.objects.get(id=room_id)
        except Exception as e:
            raise Exception('Room does not exists')

        assert room.owner_id == user.id, 'User is not the owner of group to add member'

        serializer = RoomSerializer(room, data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Room.objects.get(id=room_id)
        

    def get_all_rooms(self, user: CustomUser) -> Room:
        assert user, 'User can not be None'

        return Room.objects.filter(owner_id=user.id)


class RoomMembershipService:

    def __init__(self) -> None:
        pass


    def get_members(self, room_id: str, user: CustomUser) -> RoomMembershipSerializer:
        assert room_id, 'Room Id can not be None'
        assert user, 'User can not be None'

        room = Room.objects.filter(id=room_id)

        assert room, 'Room does not exists'

        details = RoomMembership.objects.filter(room_id=room_id)
        serializer = RoomMembershipSerializer(details, many=True)
        return serializer.data


    def add_member(self, serializer: RoomMembershipSerializer, user: CustomUser) -> RoomMembership:
        assert serializer, 'Serializer can not be None'
        assert user, 'User can not be None'

        room_id = serializer.data.get('room_id', None)
        user_id = serializer.data.get('user_id', None)

        room = Room.objects.get(id=room_id)

        assert room, 'Room does not exists'
        assert room.owner_id == user.id, 'User is not the owner of group to add member'

        membership = RoomMembership(room_id=room_id, user_id=user_id)
        membership.save()
        return membership


    def remove_member(self, room_id: str, user_id: str, user: CustomUser) -> bool:
        assert room_id, 'Room Id can not be None'
        assert user_id, 'User Id can not be None'
        assert user, 'User can not be None'

        # Get room and check the owner
        room = Room.objects.get(id=room_id)

        assert room, 'Room does not exists'
        membership = RoomMembership(user_id=user_id, room_id=room_id)
        membership.delete()

        # Create membership
        return True

    def get_user_rooms(self, user: CustomUser) -> bool:
        assert user, 'User should not be None'

        return RoomMembership.objects.filter(user_id=user.id)

