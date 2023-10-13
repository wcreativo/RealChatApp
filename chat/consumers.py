import json
import redis

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        await self.accept()
        messages = self.redis.lrange(self.room_group_name, 0, -1)
        for message in messages:
            await self.send(text_data=json.dumps({"message": message}))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.redis.rpush(self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name, {"type":"chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))