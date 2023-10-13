from rest_framework import serializers

class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    room_name = serializers.CharField(max_length=255) 