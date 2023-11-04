from django.shortcuts import render
from django.http.request import HttpRequest


def test(request: HttpRequest):
    return render(request,  template_name='chat/test.html')


def index(request: HttpRequest):
    return render(request, template_name='chat/index.html')


def room(request: HttpRequest, room_name: str):
    return render(request, template_name='chat/room.html', context={'room_name': room_name})


