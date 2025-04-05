import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer

ANNOUNCEMENTS_FILE = "announcements.json"

class AnnounceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("announcements", self.channel_name)

        announcements = self.load_announcements()
        for ann in announcements:
            await self.send(text_data=json.dumps(ann))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("announcements", self.channel_name)

    async def receive(self, text_data):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
            self.save_announcement(data)
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

    def save_announcement(self, data):
        announcements = self.load_announcements()
        announcements.append(data)
        with open(ANNOUNCEMENTS_FILE, "w") as f:
            json.dump(announcements, f, indent=4)

    def load_announcements(self):
        if not os.path.exists(ANNOUNCEMENTS_FILE):
            return []
        with open(ANNOUNCEMENTS_FILE, "r") as f:
            return json.load(f)
