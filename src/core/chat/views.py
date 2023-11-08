from django.shortcuts import render
from django.http.request import HttpRequest

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from auth_core.authentication import JwtAuthentication


class TestAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        return Response({'message': 'Server running successfully'})


def index(request: HttpRequest):
    return render(request, template_name='chat/index.html')


def room(request: HttpRequest, room_name: str):
    return render(request, template_name='chat/room.html', context={'room_name': room_name})


