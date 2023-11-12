from django.contrib.auth.models import AnonymousUser
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import json

from auth_core.models import CustomUser
from chat.models import Room


@database_sync_to_async
def get_room(room_id: str, user: CustomUser) -> Room:
    
    return Room.objects.filter(id=room_id, owner_id=user.id, room_status='Open').first()
    

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        room = await get_room(self.room_id, self.scope['user'])

        if isinstance(self.scope['user'], (AnonymousUser, UserLazyObject)) or room is None:
            return None
        
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()
        await self.send(json.dumps({'username': self.scope['user'].username, 'messageType': 'username'}))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        return super().disconnect(code)


    # Receives message from Web socket
    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)['message']

        # Consumer should have equivalent method to the type passed
        await self.channel_layer.group_send(self.room_id, {"type": "chat.message", "message": message, 'username': self.scope['user'].username})


    # This receives message from Channel group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message'], 'username': event['username']}))

        
