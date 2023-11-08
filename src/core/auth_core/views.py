from rest_framework.generics import GenericAPIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.permissions import AllowAny

from auth_core.serializers import RegisterSerializer, RegisterResponseSerializer, LoginSerializer
from auth_core.services import AuthService



class UserRegisterationAPIView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request: HttpRequest) -> Response:

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # Create model
            auth = AuthService()
            user = auth.register(serializer)

            # Return created model
            if user is None:
                return Response('Failed to create the user', status=HTTP_400_BAD_REQUEST)

            response_serializer = RegisterResponseSerializer(instance=user)
            return Response(response_serializer.data, status=HTTP_201_CREATED)

        return Response('Please provide all required info', status=HTTP_400_BAD_REQUEST)


class UserLoginAPIView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: HttpRequest) -> Response:

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            auth = AuthService()
            token = auth.login(serializer)
        except Exception as e:
            return Response(str(e), status=HTTP_401_UNAUTHORIZED)

        return Response({'token': token}, status=HTTP_200_OK)
