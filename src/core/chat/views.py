from django.shortcuts import render
from django.http.request import HttpRequest
from typing_extensions import Any

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated

from auth_core.authentication import JwtAuthentication
from chat.services import RoomService
from chat.serializers import RoomCreateSerializer, CustomUserSerializer
from chat.serializers import RoomSerializer

class UserDetailsAPIView(GenericAPIView):

    def get(self, request: HttpRequest): 
        try:
            print(request.user)
            serializer = CustomUserSerializer(instance=request.user)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TestAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        return Response({'message': 'Server running successfully'})


class RoomAPIView(GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        self.room_service = RoomService()
        super().__init__(**kwargs)

    def post(self, request: HttpRequest) -> Response:
        try:
            serializer = RoomCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            room = self.room_service.create_room(serializer.data.get('room_name'), request.user)
            room_serializer = RoomSerializer(room)
            return Response(room_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request: HttpRequest) -> Response:
        try:
            user = request.user
            rooms = self.room_service.get_all_rooms(user)
            result = []

            for room in rooms:
                serializer = RoomSerializer(room)
                result.append(serializer.data)

            return Response(result, status=HTTP_200_OK)

        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request: HttpRequest) -> Response:
        try:
            id = request.data.get('room_id', None)
            status = request.data.get('room_status', None)

            assert id, 'Id should not be None'
            assert status, 'Status should not be None'

            room = self.room_service.update_status(request.user, id, status)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=HTTP_200_OK)

        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)




