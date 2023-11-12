from chat.models import Room
from auth_core.models import CustomUser

class RoomService:
    def __init__(self) -> None:
        pass

    def create_room(self, room_name: str, user: CustomUser) -> Room:
        assert room_name, 'Room name can not be None'
        assert user, 'User can not be None'


        new_room = Room(room_name=room_name, owner_id=user.id, room_status='Closed')
        new_room.save()

        return new_room

    def get_all_rooms(self, user: CustomUser) -> Room:
        assert user, 'User can not be None'

        return Room.objects.filter(owner_id=user.id)


    def update_status(self, user: CustomUser, room_id: str, status: str) -> Room:
        room = Room.objects.filter(owner_id=user.id, id=room_id).first()

        assert room, 'User does not have permission to update this room'

        room.room_status = status
        room.save()

        return room

        