import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AnnounceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("announcements", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("announcements", self.channel_name)

    async def receive(self, text_data):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
            message = data.get('message', '')

            # Broadcast message
            await self.channel_layer.group_send(
                "announcements",
                {
                    "type": "send_message",
                    "message": message
                }
            )
        except json.JSONDecodeError:
            print("Received invalid JSON:", text_data)
    async def send_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
