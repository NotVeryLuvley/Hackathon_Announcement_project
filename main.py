import kivy
import threading
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
import time

import asyncio
import websockets
import json
# {"title": input("What is the title?: "), "desc": input("What is the description?: "), "tag": input("What is the tag?: "), "msgtype": input("What type of message is this?: ")}
# Have a way to get data from adding announcements
async def send_announcement(title, description, tag, origin):
    uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
    message = json.dumps({
        "title": title, 
        "desc": description, 
        "tag": tag, 
        "origin": origin
    }) 
    async with websockets.connect(uri) as websocket: #waits until it connects with the websocket
        await websocket.send(message) # sends the message
        # print(f"Sent: {message}")


# Get the announcements
# async def receive_announcement():
#     uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
#     async with websockets.connect(uri) as websocket: #waits until it connects with the websocket

#         response = json.loads(await websocket.recv()) #waits until it gets a message from the server
        
#         return response
    

#     asyncio.run(websocket_client())


Builder.load_file("main.kv")


class AnnouncementWidget(BoxLayout):
    def __init__(self, title, description, date, tag, origin, **kwargs):
        super().__init__(**kwargs)
        self.ids.title_label.text = title
        self.ids.description_label.text = description
        self.ids.date_label.text = date
        self.ids.tag_label.text = tag
        self.ids.origin_label.text = "From: " + origin

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#Main loop
class AnnouncementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.announcements = [
            ("Science Fair Reminder", "Submissions due by next Monday.", "2025-03-20 12:00", "Reminder", "Schience Club"),
            ("School Closure", "School will be closed on Friday due to weather conditions.", "2025-04-01", "Important", "School Board"),
            ("Parent-Teacher Meeting", "Meeting scheduled for next Wednesday.", "2025-03-30", "Event", "School Board"),
            ("Cafeteria Menu", "New menu has been updated on the school website.", "2025-03-28", "Notice", "Cafeteria")
        ]

        self.load_announcements()
        
        threading.Thread(target=self.start_websocket_listener, daemon=True).start()
        
        check_time_interval = 3600
        Clock.schedule_interval(self.cleanup_old_announcements, check_time_interval)  # 3600 seconds = 1 hour

    def cleanup_old_announcements(self, dt):
        #Remove announcements older than 2 weeks
        current_time = datetime.datetime.now()
        two_weeks_ago = current_time - datetime.timedelta(days=14)
        
        # Filter out announcements older than 2 weeks
        self.announcements = [
            announcement for announcement in self.announcements
            if self._parse_date(announcement[2]) > two_weeks_ago
        ]
        
        # Reload announcements
        self.load_announcements()
    
    def _parse_date(self, date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                # if fails, reaturn old date to make sure it works
                return datetime.datetime(1900, 1, 1)

    def load_announcements(self, search_term=None):
        self.ids.announcement_layout.clear_widgets()
        
        # Filter announcements based on search term
        filtered_announcements = self.announcements
        if search_term and search_term.strip():
            search_term = search_term.lower()
            filtered_announcements = [
                announcement for announcement in self.announcements
                if search_term in announcement[4].lower()  # Search in origin part
            ]
        
        # Display filtered announcements
        for title, description, date, tag, origin in reversed(filtered_announcements):
            self.ids.announcement_layout.add_widget(AnnouncementWidget(title, description, date, tag, origin))

    def add_announcement(self, data):
        try:
            title = data.get("title", "No Title")
            description = data.get("desc", "No Description")
            tag = data.get("tag", "No Tag")
            origin = data.get("origin", "Unknown")
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            new_announcement = (title, description, date, tag, origin)
            self.announcements.append(new_announcement)
            self.load_announcements()
        except Exception as e:
            print(f"Error adding announcement: {e}")

    def start_websocket_listener(self):
        asyncio.run(self.websocket_loop())

    async def websocket_loop(self):
        uri = "ws://127.0.0.1:55356/ws/announce/"
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    print("Connected to WebSocket server.")
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        Clock.schedule_once(lambda dt: self.add_announcement(data))
            except Exception as e:
                print(f"WebSocket error: {e}. Retrying in 3 seconds...")
                await asyncio.sleep(3)

class AddAnnouncementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#Main Loop
class AnnouncementApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_admin = False
    
    def build(self):
        # Create a screen manager
        sm = ScreenManager()
        
        # Add screens to the manager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AnnouncementScreen(name='announcements'))
        sm.add_widget(AddAnnouncementScreen(name='add_announcement'))
        
        return sm
    
    def login_as_admin(self):
        self.is_admin = True
        self.show_announcement_screen()
    
    def login_as_student(self):
        self.is_admin = False
        self.show_announcement_screen()
    
    def show_add_announcement_screen(self):
        self.root.current = 'add_announcement'

    def setup_announcement(self):
        try:
            # Get the input values from the text fields
            add_screen = self.root.get_screen('add_announcement')
            title = add_screen.ids.title_input.text
            description = add_screen.ids.description_input.text
            tag = add_screen.ids.tag_input.text
            origin = add_screen.ids.origin_input.text
            
            # Check if any field is empty
            if not title or not description or not tag or not origin:
                # display all fields must be filled out type thing
                add_screen.ids.error_label.opacity = 1
                return
            
            
            asyncio.run(send_announcement(title, description, tag, origin))

            add_screen.ids.error_label.opacity = 0
            self.show_announcement_screen()

            # get rid of inputs
            add_screen.ids.title_input.text = ""
            add_screen.ids.description_input.text = ""
            add_screen.ids.tag_input.text = ""
            add_screen.ids.origin_input.text = ""
            
            
        except Exception as e:
            print(f"Error: {e}")
    
    def search_announcement(self):
        # Get the search term from the input field
        announcement_screen = self.root.get_screen('announcements')
        search_term = announcement_screen.ids.search_input.text
        
        # Reload announcements with that search term
        announcement_screen.load_announcements(search_term)

    def show_announcement_screen(self):
        # Switch back to the announcement screen
        add_screen = self.root.get_screen('add_announcement')
        add_screen.ids.error_label.opacity = 0
        self.root.current = 'announcements'

        self.root.get_screen('add_announcement').ids.title_input.text = ""
        self.root.get_screen('add_announcement').ids.description_input.text = ""
        self.root.get_screen('add_announcement').ids.tag_input.text = ""
        self.root.get_screen('add_announcement').ids.origin_input.text = ""
        
        # Show or hide the add announcement button based on admin or student
        announcement_screen = self.root.get_screen('announcements')
        if self.is_admin:
            announcement_screen.ids.add_announcement_button.opacity = 1
            announcement_screen.ids.add_announcement_button.disabled = False
        else:
            announcement_screen.ids.add_announcement_button.opacity = 0
            announcement_screen.ids.add_announcement_button.disabled = True

AnnouncementApp().run()
