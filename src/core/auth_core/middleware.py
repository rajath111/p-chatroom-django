from channels.db import database_sync_to_async
from django.conf import settings

import jwt

from auth_core.models import CustomUser


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



class WebSocketAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        scope['user'] = await get_user(get_access_token(scope["query_string"]))

        return await self.app(scope, receive, send)




