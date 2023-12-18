from django.contrib.auth.models import AnonymousUser
from channels.auth import UserLazyObject
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from enum import Enum

from chat.services import ConsumerService, MessageService
from chat.serializers import MessageSerializer

class MessageType:
    BROADCAST_MESSAGE = 1
    USERNAME = 2
    USER_MESSAGE = 3


class Message:
    def __init__(self) -> None:
        self.messageType = None
        self.data = None


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def connect(self):

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.consumer_service = ConsumerService()
        self.message_service = MessageService()

        room = await self.consumer_service.get_room(self.room_id, self.scope['user'])

        if isinstance(self.scope['user'], (AnonymousUser, UserLazyObject)) or room is None:
            return None
        
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()
        await self.send(json.dumps({'data': {'username': self.scope['user'].username}, 'messageType': MessageType.USERNAME}))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        return super().disconnect(code)


    # Receives message from Web socket
    async def receive(self, text_data=None, bytes_data=None):
        data: Message = json.loads(text_data)

        if data['messageType'] == MessageType.USER_MESSAGE:
            message = data['data']['message']

            # Create message in DB
            message = await self.message_service.create_message(self.scope['user'].id, self.room_id, message)
            
            # Consumer should have equivalent method to the type passed
            await self.channel_layer.group_send(self.room_id, {"type": "chat.message", "data": message})


    # This receives message from Channel group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'data': event['data'], 'messageType': MessageType.BROADCAST_MESSAGE}))

        
