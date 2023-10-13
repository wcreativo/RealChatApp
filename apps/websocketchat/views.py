from django.shortcuts import render

def index(request):
    return render(request, "websocketchat/index.html")


def room(request, room_name):
    return render(request, "websocketchat/room.html", {"room_name": room_name})