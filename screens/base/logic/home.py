# screens/home.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
import datetime
import os

class HomeScreen(Screen):
    """
    The home screen of the application.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'home.kv')
        Builder.load_file(kv_path)

    def go_to_check_in_screen(self, instance):
        current_time = datetime.datetime.now()
        if current_time.weekday() >= 5:  # 5 and 6 correspond to Saturday and Sunday
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'abc_please'
        elif current_time.hour < 12:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'mindfulness'
        elif current_time.hour > 18:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'evening_diary'
        else:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'choose_checkin'

    def go_to_voice_diary_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'suicidal'

    def go_to_help_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'crisis'

    def go_to_settings_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'settings'
