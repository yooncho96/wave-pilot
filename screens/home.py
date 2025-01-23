# screens/home.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout

from data.db_helper import DBHelper
import datetime

class HomeScreen(Screen):
    """
    The home screen of the application.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title_label = Label(text="Welcome.", font_size=24)
        layout.add_widget(title_label)

        image = Image(source='path/to/image.png')
        layout.add_widget(image)

        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=10)

        check_in_btn = Button(text="Check In", size_hint=(1, 0.1))
        check_in_btn.bind(on_release=self.go_to_check_in_screen)
        button_layout.add_widget(check_in_btn)

        voice_diary_btn = Button(text="Voice Diary", size_hint=(1, 0.1))
        voice_diary_btn.bind(on_release=self.go_to_voice_diary_screen)
        button_layout.add_widget(voice_diary_btn)

        help_btn = Button(text="Help", size_hint=(1, 0.1))
        help_btn.bind(on_release=self.go_to_help_screen)
        button_layout.add_widget(help_btn)

        layout.add_widget(button_layout)

        anchor_layout = AnchorLayout(anchor_x='right', anchor_y='top')
        settings_btn = Button(text="Settings", size_hint=(None, None), size=(50, 50))
        settings_btn.bind(on_release=self.go_to_settings_screen)
        anchor_layout.add_widget(settings_btn)
        layout.add_widget(anchor_layout)

        self.add_widget(layout)

    def go_to_check_in_screen(self, instance):
        current_time = datetime.datetime.now()
        if current_time.weekday() >= 5:  # 5 and 6 correspond to Saturday and Sunday
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'abc_please'
        elif current_time.hour < 12:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'mindfulness'
        else:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'evening_diary'

    def go_to_voice_diary_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'suicidal'

    def go_to_help_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'crisis'

    def go_to_settings_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'settings'
