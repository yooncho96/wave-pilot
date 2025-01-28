from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import calendar
import datetime
import time
from plyer import notification

class SetReminderScreen(Screen):

    def __init__(self, **kwargs):
        super(SetReminderScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        reminder_label = Label(text="That's okay! When would be the best time for me to remind you?", font_size=18)
        layout.add_widget(reminder_label)

        day_label = Label(text="On:", font_size=18)
        layout.add_widget(day_label)

        self.day_spinner = Spinner(
            text='Day of the week',
            values=('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.day_spinner)

        week_label = Label(text="of:", font_size=18)
        layout.add_widget(week_label)

        self.week_spinner = Spinner(
            text='which',
            values=('this', 'next'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.week_spinner)

        time_label = Label(text="at", font_size=18)
        layout.add_widget(time_label)

        self.time_input = TextInput(hint_text="e.g., 12:00", size_hint=(1, 0.1))
        layout.add_widget(self.time_input)

        set_btn = Button(text="Set Reminder", size_hint=(1, 0.1))
        set_btn.bind(on_release=self.on_set())
        layout.add_widget(set_btn)

        self.add_widget(layout)
    
    def get_chosen_datetime(self):
        chosen_day = self.day_spinner.text
        chosen_week = self.week_spinner.text
        chosen_time = self.time_input.text

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

    def send_notification():
        notification.notify(
            title="Reminder",
            message="I think you promised to try something today.",
            timeout=10
        )
    
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
        self.manager.current = "home_screen"