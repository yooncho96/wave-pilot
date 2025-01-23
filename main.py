# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Import our screens
from screens.home import HomeScreen
from screens.voice_diary.assess_emotion.record import SpeechScreen
from screens.voice_diary.assess_emotion.confirm_emotion import EmotionDataScreen

class MyScreenManager(ScreenManager):
    """
    The screen manager to handle navigation between HomeScreen, SpeechScreen, and EmotionDataScreen.
    """
    pass

class MyApp(App):
    """
    Main Kivy Application
    """
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(SpeechScreen(name="speech_screen"))
        sm.add_widget(EmotionDataScreen(name="emotion_data_screen"))
        return sm

if __name__ == "__main__":
    MyApp().run()
