from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Get room name from URL
        # self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Create chat room name with suffix to room name
        # self.room_group_name = f'chat_{self.room_name}'

        # Added the channel to the group, with group name is same as room name
        # self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accect the socket
        self.accept()

    
    def disconnect(self, code):
        # self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        return super().disconnect(code)


    # Receives message from Web socket
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        print('Message received:', message)
        # Sends message back to User
        self.send(text_data=json.dumps({'message': message}))
