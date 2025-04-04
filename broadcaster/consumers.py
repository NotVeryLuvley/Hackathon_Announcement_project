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
            date = data.get("date", "No Date")
            tag = data.get("tag", "No Tag")
            msgtype = data.get("msgtype", "No Type")

            await self.channel_layer.group_send(
                "announcements",
                {
                    "type": "send_message",
                    "title": title,
                    "desc": desc,
                    "date": date,
                    "tag": tag,
                    "msgtype": msgtype,
                }
            )
        except json.JSONDecodeError:
            print("Received invalid JSON:", text_data)
    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "title": event.get("title", ""),
            "desc": event.get("desc", ""),
            "date": event.get("date", ""),
            "tag": event.get("tag", ""),
            "msgtype": event.get("msgtype", "")
        }))
