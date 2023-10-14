from rest_framework import serializers
from .models import Chatroom


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    room_name = serializers.CharField(max_length=255)


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = "__all__"
