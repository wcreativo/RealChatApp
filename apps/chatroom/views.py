from channels.layers import get_channel_layer
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from .serializers import SendMessageSerializer, ChatRoomSerializer
from .models import Chatroom
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class ChatRoomViewSet(ModelViewSet):
    queryset = Chatroom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = request.data["message"]
            room_name = request.data["room_name"]

            try:
                Chatroom.objects.get(name=room_name)
            except Chatroom.DoesNotExist:
                return Response(
                    {"error": f"Room name {room_name} doesn't exist!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            channel_layer = get_channel_layer()
            room_group_name = f"chat_{room_name}"
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                },
            )
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
