from typing import Any
from rest_framework.generics import GenericAPIView
from rest_framework.request import HttpRequest
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response

from chat.services import MessageService
from chat.serializers import MessageSerializer

class MessageAPIVew(GenericAPIView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.message_service = MessageService()


    def get(self, request: HttpRequest, room_id: int, n_count: int):
        try:
            messages = self.message_service.get_last_n_messages(room_id, int(n_count))

            result = []

            for mess in messages:
                serializer = MessageSerializer(mess)
                result.append(serializer.data)

            return Response(result, status=HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)