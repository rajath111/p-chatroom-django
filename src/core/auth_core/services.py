from rest_framework.exceptions import AuthenticationFailed

from auth_core.serializers import RegisterSerializer, LoginSerializer
from auth_core.models import CustomUser
from auth_core.authentication import JwtAuthentication

class AuthService:

    def register(self, registerData: RegisterSerializer) -> CustomUser:
        username = registerData.data['username']
        user = CustomUser.objects.filter(username=username).first()

        if user is not None:
            return None

        user = CustomUser(username=username, password=registerData.data['password'], age=registerData.data['age'], first_name=registerData.data['first_name'], last_name=registerData.data['last_name'])
        user.save()

        return user


    def login(self, loginData: LoginSerializer) -> str:
        username = loginData.data['username']

        user = CustomUser.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User does not exists')

        if user.password == loginData.data['password']:
            return JwtAuthentication.get_token(user)

        raise AuthenticationFailed('Username and password does not match')
        
