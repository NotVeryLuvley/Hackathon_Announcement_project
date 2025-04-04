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
import datetime

Builder.load_file("main.kv")


class AnnouncementWidget(BoxLayout):  # Changed from RelativeLayout
    def __init__(self, title, description, date, tag, origin, **kwargs):
        super().__init__(**kwargs)
        self.ids.title_label.text = title
        self.ids.description_label.text = description
        self.ids.date_label.text = date
        self.ids.tag_label.text = tag
        self.ids.origin_label.text = "From: " + origin

class AnnouncementScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.announcements = [
            ("School Closure", "School wilsdfdsfs fs f dsf ds fds fd f df dv sd vsdvdsvdsfdsf ds fds l be closed on Friday due to weather conditions.", "2025-04-01", "Important", "School Board"),
            ("Parent-Teacher Meeting", "Meeting scheduled for next Wednesday.", "2025-03-30", "Event", "Student Council"),
            ("Cafeteria Menu", "New menu has been updated on the school website.", "2025-03-28", "hel from the oter side", "Computer Science"),
            ("Science Fair Reminder", "Submissions due by next Monday.", "2025-03-25", "Reminder", "Event")
        ]

        self.load_announcements()
        
        # Schedule automatic refresh every 3 seconds
        Clock.schedule_interval(self.auto_refresh, 3.0)  # 3.0 seconds interval

    def load_announcements(self):
        self.ids.announcement_layout.clear_widgets()
        for title, description, date, tag, origin in reversed(self.announcements):
            self.ids.announcement_layout.add_widget(AnnouncementWidget(title, description, date, tag, origin))

    def refresh_announcements(self):
        new_announcement = ("New Announcement", "This is a newly added announcement!", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "New", "School Board")
        self.announcements.append(new_announcement)
        self.ids.announcement_layout.add_widget(AnnouncementWidget(*new_announcement))
        self.load_announcements()
        
    def auto_refresh(self, dt):
        """Function called automatically every 3 seconds"""
        self.refresh_announcements()

class AnnouncementApp(App):
    def build(self):
        return AnnouncementScreen()

if __name__ == '__main__':
    AnnouncementApp().run()