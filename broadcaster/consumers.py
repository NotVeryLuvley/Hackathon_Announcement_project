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
            title = data.get("title", "No Title")
            desc = data.get("desc", "No Description")
            tag = data.get("tag", "No Tag")
            origin = data.get("origin", "No Type")

            await self.channel_layer.group_send(
                "announcements",
                {
                    "type": "send_message",
                    "title": title,
                    "desc": desc,
                    "tag": tag,
                    "origin": origin,
                }
            )
        except json.JSONDecodeError:
            print("Received invalid JSON:", text_data)
    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "title": event.get("title", ""),
            "desc": event.get("desc", ""),
            "tag": event.get("tag", ""),
            "origin": event.get("origin", "")
        }))
