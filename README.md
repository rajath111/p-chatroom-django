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

# Adding channel support for Websocket
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


## Create User and group


## Broadcast message to group


## Credits and Resources
While creating this application, I have refered to the following resources. For more details please refer these.

1. https://www.youtube.com/watch?v=F4nwRQPXD8w&list=WL&index=20&t=2099s
2. https://channels.readthedocs.io/en/latest/introduction.html
3. 