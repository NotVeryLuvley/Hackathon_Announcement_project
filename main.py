import kivy
kivy.require('2.0.0')  # Specify the minimum Kivy version required
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout  # Changed from RelativeLayout
from kivy.clock import Clock  # Add Clock import for scheduling
from kivy.uix.screenmanager import ScreenManager, Screen
import datetime

import asyncio
import websockets
import json
# {"title": input("What is the title?: "), "desc": input("What is the description?: "), "tag": input("What is the tag?: "), "msgtype": input("What type of message is this?: ")}
async def send_announcement():
    uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
    message = json.dumps({"title": "What is the title?: ", "desc": "What is the description?: ", "tag": "What is the tag?: ", "origin": "What type of message is this?: "}) #change the input date to a way to get the date from the os on android
    async with websockets.connect(uri) as websocket: #waits until it connects with the websocket
        await websocket.send(message) # sends the message
        # print(f"Sent: {message}")



async def receive_announcement():
    uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
    async with websockets.connect(uri) as websocket: #waits until it connects with the websocket

        response = json.loads(await websocket.recv()) #waits until it gets a message from the server
        
        return response
    

#     asyncio.run(websocket_client())


Builder.load_file("main.kv")


class AnnouncementWidget(BoxLayout):  # Changed from RelativeLayout
    def __init__(self, title, description, date, tag, origin, **kwargs):
        super().__init__(**kwargs)
        self.ids.title_label.text = title
        self.ids.description_label.text = description
        self.ids.date_label.text = date
        self.ids.tag_label.text = tag
        self.ids.origin_label.text = "From: " + origin

class AnnouncementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.announcements = [
            ("School Closure", "School wilsdfdsfs fs f dsf ds fds fd f df dv sd vsdvdsvdsfdsf ds fds l be closed on Friday due to weather conditions.", "2025-04-01", "Important", "School Board"),
            ("Parent-Teacher Meeting", "Meeting scheduled for next Wednesday.", "2025-03-30", "Event", "Student Council"),
            ("Cafeteria Menu", "New menu has been updated on the school website.", "2025-03-28", "hel from the oter side", "Computer Science"),
            ("Science Fair Reminder", "Submissions due by next Monday.", "2025-03-25", "Reminder", "Event")
        ]

        print(self.announcements)

        self.load_announcements()
        
        # Schedule automatic refresh every 3 seconds
        Clock.schedule_interval(self.auto_refresh, 3.0)  # 3.0 seconds interval

    def load_announcements(self):
        self.ids.announcement_layout.clear_widgets()
        for title, description, date, tag, origin in reversed(self.announcements):
            self.ids.announcement_layout.add_widget(AnnouncementWidget(title, description, date, tag, origin))

    def refresh_announcements(self):
        # new_announcement = ("New Announcement", "This is a newly added announcement!", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "New", "School Board")
        # self.announcements.append(new_announcement)
        # self.ids.announcement_layout.add_widget(AnnouncementWidget(*new_announcement))
        try:
            new_announcement = asyncio.run(receive_announcement())
            self.title = new_announcement["title"]
            self.description = new_announcement["desc"]
            self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.tag = new_announcement["tag"]
            self.origin = new_announcement["origin"]
            new_announcement = (self.title, self.description, self.date, self.tag, self.origin)
            self.announcements.append(new_announcement)
            self.load_announcements()
        except Exception as e:
            print(f"Error: {e}")
        
        
        
    def auto_refresh(self, dt):
        """Function called automatically every 3 seconds"""
        self.refresh_announcements()

class AddAnnouncementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AnnouncementApp(App):
    def build(self):
        # Create a screen manager
        sm = ScreenManager()
        
        # Add screens to the manager
        sm.add_widget(AnnouncementScreen(name='announcements'))
        sm.add_widget(AddAnnouncementScreen(name='add_announcement'))
        
        return sm
    
    def show_add_announcement_screen(self):
        # Switch to the add announcement screen
        self.root.current = 'add_announcement'

    def send_announcement(self):
        try:
            (asyncio.run(send_announcement()))
        except Exception as e:
            print(f"Error: {e}")

    def show_announcement_screen(self):
        # Switch back to the announcement screen
        self.root.current = 'announcements'

if __name__ == '__main__':
    AnnouncementApp().run()

