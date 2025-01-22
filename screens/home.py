# screens/home.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from data.db_helper import DBHelper

class HomeScreen(Screen):
    """
    The home screen of the application.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title_label = Label(text="Welcome.", font_size=24)
        layout.add_widget(title_label)

        

        diary_btn = Button(text="Diary", size_hint=(1, 0.1))
        diary_btn.bind(on_release=self.go_to_diary_screen)
        layout.add_widget(diary_btn)

        check_in_btn = Button(text="Check-in", size_hint=(1, 0.1))
        check_in_btn.bind(on_release=self.go_to_check_in_screen)
        layout.add_widget(check_in_btn)

        self.add_widget(layout)
    
    def go_to_diary_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "speech_screen"
    
    def go_to_check_in_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "emotion_data_screen"
