from django.http.request import HttpRequest
from typing_extensions import Any

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated

from auth_core.authentication import JwtAuthentication
from chat.services import RoomService
from chat.serializers import RoomCreateSerializer, CustomUserSerializer, RoomMembershipSerializer
from chat.serializers import RoomSerializer
from chat.models import Room
from chat.services import RoomMembershipService


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


class RoomDetailAPIView(GenericAPIView):
    def __init__(self, **kwargs: Any) -> None:
        self.room_service = RoomService()
        super().__init__(**kwargs)


    def get(self, request: HttpRequest, room_id: str) -> Response:
        try:
            room = self.room_service.get_room(room_id, request.user)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    

    def delete(self, request: HttpRequest, room_id: str) -> Response:
        try:
            self.room_service.delete_room(room_id, request.user)
            return Response(status=HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request: HttpRequest, room_id: str) -> Response:
        try:
            room = self.room_service.update_room(room_id, request.user, request.data)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class RoomMembershipApiView(GenericAPIView):
    def __init__(self, **kwargs: Any) -> None:
        self.room_membership_service = RoomMembershipService()
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> Response:
        try:
            memberships = self.room_membership_service.get_user_rooms(request.user)
            return Response([RoomMembershipSerializer(member).data for member in  memberships], status=HTTP_200_OK)

        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


    
    def post(self, request: HttpRequest) -> Response:
        try: 
            serializer = RoomMembershipSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            membership = self.room_membership_service.add_member(serializer, request.user)
            response = RoomMembershipSerializer(membership)
            return Response(response.data, status=HTTP_200_OK)

        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class RoomMembershipDetailAPIView(GenericAPIView):
    def __init__(self, **kwargs: Any) -> None:
        self.room_membership_service = RoomMembershipService()
        super().__init__(**kwargs)
    
    def get(self, request: HttpRequest, room_id) -> Response:
        try:
            room_details = self.room_membership_service.get_members(room_id, request.user)
            return Response(room_details, status=HTTP_200_OK)

        except Exception as e:
            return Response({'messsage': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)



