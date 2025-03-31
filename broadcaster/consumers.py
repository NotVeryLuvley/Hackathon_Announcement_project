import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AnnouncerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("announcements", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("announcements", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send message to group
        await self.channel_layer.group_send(
            "announcements",
            {
                "type": "broadcast_message",
                "message": message,
            }
        )

    async def broadcast_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({"message": message}))