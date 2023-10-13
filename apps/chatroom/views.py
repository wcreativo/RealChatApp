from django.shortcuts import render
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from .serializers import SendMessageSerializer
from .models import Chatroom
from rest_framework import status


def index(request):
    return render(request, "chatroom/index.html")


def room(request, room_name):
    return render(request, "chatroom/room.html", {"room_name": room_name})


class SendMessageView(APIView):

    serializer_class = SendMessageSerializer

    def post(self, request, *args, **kwargs):
        message = request.data["message"]
        room_name = request.data["room_name"]

        try:
            Chatroom.objects.get(name=room_name)
        except Chatroom.DoesNotExist():
            return Response({"error": f"{room_name} doesn't exists!"}, status=status.HTTP_400_BAD_REQUEST)

        if message:
            channel_layer = get_channel_layer()
            room_group_name = f"chat_{room_name}"
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'send.message',
                    'message': message,
                }
            )
            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

