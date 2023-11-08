from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.conf import settings
import jwt
from datetime import datetime, timedelta

from auth_core.models import CustomUser

class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # Get Auth header
        token = get_authorization_header(request).decode().replace('Bearer ', '').encode()

        if token is None:
            raise AuthenticationFailed('Auth token is not found')

        # Validate Token
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e: 
            raise ParseError('Invalid Signature')
        if decoded_token['expires'] < datetime.now().timestamp():
            raise AuthenticationFailed('Token Expired')

        # Return User
        username = decoded_token['username']

        return (CustomUser.objects.get(username=username), None)


    @staticmethod
    def get_token(user: CustomUser):
        # HS256 is synnetric algorithm
        token = jwt.encode(payload={'username': user.username, 'expires': int((datetime.now() + timedelta(hours=3)).timestamp())
        }, key=settings.SECRET_KEY, algorithm='HS256')
        return token


    def authenticate_header(self, request):
        return 'Basic realm=api'