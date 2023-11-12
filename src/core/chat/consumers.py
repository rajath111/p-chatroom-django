from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import json
import random
import jwt

from auth_core.models import CustomUser
from chat.models import Room

@database_sync_to_async
def get_user(access_token: str) -> CustomUser:
    try:
        decoded_token = jwt.decode(access_token, key=settings.SECRET_KEY, algorithms=['HS256'])
        username = decoded_token['username']
        return CustomUser.objects.get(username=username)

    except Exception as e:
        return None

def get_access_token(query_string: bytearray) -> str:
    try:
        query_string = query_string.decode('utf-8')
        query_params = query_string.split('&')
        for param in query_params:
            key, value = param.split('=')
            if key == 'access_token':
                return value

        return None

    except Exception as e:
        return None

@database_sync_to_async
def get_room(room_id: str, user: CustomUser) -> Room:
    
    return Room.objects.filter(id=room_id, owner_id=user.id).first()
    

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_name = str(random.randint(1, 10000))
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        self.user = await get_user(get_access_token(self.scope['query_string']))
        room = await get_room(self.room_id, self.user)

        # self.scope['query_strings']
        if isinstance(self.user, (AnonymousUser, UserLazyObject)) or room is None:
            # self.close()
            return None
        
        # Added the channel to the group, with group name is same as room name
        await self.channel_layer.group_add(self.room_id, self.channel_name)

        # Accect the socket
        await self.accept()

        await self.send(json.dumps({'username': self.user_name, 'messageType': 'username'}))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        return super().disconnect(code)


    # Receives message from Web socket
    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)['message']

        # Consumer should have equivalent method to the type passed
        await self.channel_layer.group_send(self.room_id, {"type": "chat.message", "message": message, 'username': self.user.username})


    # This receives message from Channel group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message'], 'username': event['username']}))

        
