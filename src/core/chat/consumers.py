from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = str(random.randint(1, 10000))
        # Get room name from URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Create chat room name with suffix to room name
        self.room_group_name = f'chat_{self.room_name}'

        # Added the channel to the group, with group name is same as room name
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        # Accect the socket
        self.accept()
        
        self.send(json.dumps({'message': 'username: ' + self.user_name}))

    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        return super().disconnect(code)


    # Receives message from Web socket
    def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)['message']
        print(self.scope['user'])

        # Consumer should have equivalent method to the type passed
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat.message", "message": f"{self.user_name} : {message}"})
        
        # Sends message back to User
        # self.send(text_data=json.dumps({'message': message}))


    # This receives message from Channel group
    def chat_message(self, event):
        self.send(text_data=json.dumps({'message': event['message']}))

        
