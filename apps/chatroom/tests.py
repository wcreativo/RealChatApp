from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from asgiref.testing import ApplicationCommunicator
from .models import Chatroom
from rest_framework.test import APIClient


class SendMessageViewTestCase(TestCase):
    def setUp(self):
        self.room_name = "test_room"
        self.chatroom = Chatroom.objects.create(name=self.room_name)
        self.valid_message_data = {
            "room_name": self.room_name,
            "message": "Test message",
        }
        self.invalid_message_data = {
            "room_name": "non_existent_room",
            "message": "Test message",
        }
        self.valid_url = reverse("send_message")
        self.client = APIClient()

    def test_send_valid_message(self):
        response = self.client.post(
            self.valid_url, data=self.valid_message_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"success": True})

    def test_send_message_to_non_existent_room(self):
        response = self.client.post(
            self.valid_url, data=self.invalid_message_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "error": f"Room name {self.invalid_message_data['room_name']} doesn't exist!"
            },
        )

    def test_channel_layer_message_send(self):
        communicator = ApplicationCommunicator(
            self.application,
            {"type": "websocket.connect"},
            scope={"type": "websocket.connect"},
        )
        communicator.scope["user"] = self.user
        communicator.scope["room_name"] = self.room_name
        communicator.scope["type"] = "websocket.connect"
        communicator.connect()
        message_data = {
            "type": "chat.message",
            "message": "Test message",
        }
        communicator.send_json_to(message_data)
        response = communicator.receive_json_from()
        self.assertEqual(response["type"], "chat.message")
        self.assertEqual(response["message"], "Test message")

    def test_invalid_data_returns_400(self):
        response = self.client.post(self.valid_url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_serializer_validation_error_returns_400(self):
        invalid_data = {
            "room_name": "test_room",
            "message": "",
        }
        response = self.client.post(self.valid_url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
