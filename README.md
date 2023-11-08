# Chat Room using Django Channels

Django channels provides support for Socket programming.
We can create group and add users to that group. Then we can broadcast the messages to that group. And can be used like a room.

![Alt Text](./doc%20resources/Async%20Request%20flow.png)

![Alt Text](./doc%20resources/Http%20and%20Socket%20Request%20Overview.png)

For HTTP views, we can set up routing in urls.py file at project file.
For Web socket connections and requets we can set up routing in routing.py in project root and update ASGI_APPLICATION property in settings.py file.


## Installing Channels
```pip install channels[daphne]```
This will install optional daphne ASGI server along with the channels package.

We can also install channels without daphne server and we can use ASGI server of choice.
```pip install channels```


## Requirements
Python 3.7+
Django 3.2+


## Configuring Channels

1. Add channels to installed apps
2. Add daphne to installed apps in array
3. Add routes, for example chat/
4. Add ASGI_APPLICATION in settings.py   
    ```ASGI_APPLICATION = '<project name>.asgi.application'```


## Setting up routes
Add routing.py in project folder.
```
from channels.auto import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, UrlRouter

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        UrlRouter(
            module_imported.ws_urlpatterns
        )
    ),
})
```

Add routing.py in chat app folder.
```
from django.urls import re_path

ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>)\w+/$', consumers.ChatRoomConsumer)
]
```

Add Chat Room Consumer in chats application, consumers.py.
```
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    pass

```

## Scope and Events
When web socket is created using channels, the scope will be created. This will presistant throughout the connection time. This inclde information like path, IP adress, user information. ```For HTTP scope lasts for single request :)```

Events represents user interactions. **Channels / ASGI applications are instantiated once per scope.**

## Consumer
Basic unit of Channels code. It is called comsumer because it consumes events :). Its like a little application. Consumers are long running, obiously! 

Underneath Channels are running on fully Asynchronous event loop.


## Creating Web socket Endpoint
1. Create a Web socket consumer
2. Add entry to routing.py file
   Use re_path instead of path
3. Add below code to asgi.py file
```
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from chat.routing import ws_urlpatterns


"websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
# AuthMiddlewareStack will add scope to the request and also populates the logged in user.
```

## Channel Layers
Channel layers allow you to talk between different instances of an application.

Use CHANNEL_LAYERS to add and configure channel layers in Django application.

```Channel layers have a purely async interface (for both send and receive); you will need to wrap them in a converter if you want to call them from synchronous code (see below).```

By default the send(), group_send(), group_add() and other functions are async functions, meaning you have to await them. If you need to call them from synchronous code, you’ll need to use the handy asgiref.sync.async_to_sync wrapper:

```
from asgiref.sync import async_to_sync

async_to_sync(channel_layer.send)("channel_name", {...})
```

## Adding channel support for Websocket
A channel is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to the channel.

A group is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.

Every consumer instance has an automatically generated unique channel name, and so can be communicated with via a channel layer.

Resource: https://channels.readthedocs.io/en/latest/tutorial/part_2.html

1. Add Channel layers
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

## Ways to add connect to Web socket in Angular
1. RXJS web socket: https://stackoverflow.com/questions/60952255/connecting-a-websocket-in-angular
2. Blog on the same: https://blog.briebug.com/blog/making-use-of-websockets-in-angular


## Adding Bootstrap to Angular App
Please refer to this awesome resource: https://www.freecodecamp.org/news/how-to-add-bootstrap-css-framework-to-an-angular-application/

## Create User and group
When socket connection is made, I am generating random user name and storing in the consumer. But, for production grade application we sholud use authenticated user and use that in scoket.

The method ```channel_layer.group_add``` will create new group if it does not exists and requires group name and channel name as parameters.

```
async def connect(self):
    # Generating random user name
    self.user_name = str(random.randint(1, 10000))
    
    # Get room name from URL, Create chat room name with suffix to room name
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'

    # Added the channel to the group, with group name is same as room name
    await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    # Accect the socket
    await self.accept()

async def disconnect(self, code):
    await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    return super().disconnect(code)
```


## Broadcast message to group
We can use ```channel_layer.group_send``` method to broadcast the message to all the channels in the group, we should specify the group name and the message which we want to broadcast.

The ```type``` value corresponds to the method name in the consumer. In the below example, the type is specified as *chat.message*, which corresponds to *chat_message* method in the consumer.

```
class ChatConsumer(AsyncWebsocketConsumer):
    # Receives message from Web socket
    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)['message']

        # Consumer should have equivalent method to the type passed
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": f"{self.user_name} : {message}"})


    # This receives message from Channel group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))
```


## Credits and Resources
While creating this application, I have refered to the following resources. For more details please refer these.

1. https://www.youtube.com/watch?v=F4nwRQPXD8w&list=WL&index=20&t=2099s
2. https://channels.readthedocs.io/en/latest/introduction.html
3. Custom JWT Auth - https://medium.com/codex/django-rest-framework-custom-jwt-authentication-backend-17bbd178b4fd#:~:text=Firstly%2C%20we%20are%20going%20to,which%20we%20call%20it%20ObtainTokenView%20.





## Adding Google Authentication to Django app
1. Create Django project and app
2. Install django-cors-headers
3. Install google-api-python-client
4. Update settings.py
   ```
    GOOGLE_CLIENT_ID = <CLIENT_ID>
    SOCIAL_SECRET = <SOCIAL_SECRET>
    CORS_ORIGIN_ALLOW_ALL = True

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsMiddleware',                          # <<< newly added line
    ]


   ```
5. Add this to middlewares
   'corsheaders.middleware.CorsMiddleware', 


6. Add a serializer
```
from django.conf import settings
from rest_framework import serializers
from library.sociallib import google
from library.register.register import register_social_user
from rest_framework.exceptions import AuthenticationFailed

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        print(user_data['aud'])
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)

```