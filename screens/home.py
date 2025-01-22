# screens/home.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class HomeScreen(Screen):
    """
    The home screen of the application.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title_label = Label(text="Welcome to My Kivy App", font_size=24)
        layout.add_widget(title_label)

        speech_btn = Button(text="Go to Speech Screen", size_hint=(1, 0.1))
        speech_btn.bind(on_release=self.go_to_speech_screen)
        layout.add_widget(speech_btn)

        show_data_btn = Button(text="Show Emotion Data", size_hint=(1, 0.1))
        show_data_btn.bind(on_release=self.show_data)
        layout.add_widget(show_data_btn)

        self.add_widget(layout)
    
    def go_to_speech_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "speech_screen"
    
    def show_data(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "emotion_data_screen"
