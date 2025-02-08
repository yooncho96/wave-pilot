from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os
import calendar
import datetime
import time
from plyer import notification

class SetReminderScreen(Screen):    
    def __init__(self, **kwargs):
        super(SetReminderScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'set_reminder.kv')
        Builder.load_file(kv_path)

    def get_chosen_datetime(self):
        chosen_day = self.ids.day_spinner.text
        chosen_week = self.ids.week_spinner.text
        chosen_time = self.ids.time_input.text

        today = datetime.date.today()
        days_ahead = (list(calendar.day_name).index(chosen_day) - today.weekday() + 7) % 7
        if chosen_week == 'next':
            days_ahead += 7

        chosen_date = today + datetime.timedelta(days=days_ahead)
        return chosen_date.strftime("%Y-%m-%d"), chosen_time

    def schedule_notification(self, date_str, time_str):
        reminder_time = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        current_time = datetime.datetime.now()
        time_diff = (reminder_time - current_time).total_seconds()
        
        if time_diff > 0:
            print(f"Thanks for promising to try! I'll remind you at {reminder_time}.")
            time.sleep(time_diff)
            self.send_notification()
        else:
            print("It looks like we are now past that time. Please enter a future time.")

    def send_notification(self):
        notification.notify(
            title="Reminder",
            message="I think you promised to try something today.",
            timeout=10
        )
        notification.bind(on_release=self.to_skill)
    
    def on_set(self, instance):
        date_str, time_str = self.get_chosen_datetime()
        self.schedule_notification(date_str, time_str)
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text="Stay safe, and talk to you later."))

        close_button = Button(text="OK", size_hint=(1, 0.2))
        popup_content.add_widget(close_button)

        popup = Popup(title="Reminder Set", content=popup_content, size_hint=(0.8, 0.4))
        close_button.bind(on_release=popup.dismiss)
        popup.open()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'home'

    def to_skill(self):
        self.manager.current = 'offer_skill'
