from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.lang import Builder
import os

from data.diary_db_Helper import DBHelper

class ConfirmEmotionScreen(Screen):

    def __init__(self, **kwargs):
        super(ConfirmEmotionScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'confirm_emotion.kv')
        Builder.load_file(kv_path)
        self.display_emotions()

    def display_emotions(self):
        db = DBHelper()
        emotion_data = db.get_emotion_data()
        db.close()

        sorted_emotions = sorted(emotion_data.items(), key=lambda x: x[1], reverse=True)
        top3_emotions = sorted_emotions[:3]

        self.ids.message_label.text = (
            "I sense these emotions in your voice diary.\n"
            "Let me know if you feel a bit differently."
        )

        for emotion, value in top3_emotions:
            emotion_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            emotion_label = Label(text=emotion, size_hint_x=0.5)
            emotion_slider = Slider(min=0, max=10, value=value, size_hint_x=0.5)
            emotion_layout.add_widget(emotion_label)
            emotion_layout.add_widget(emotion_slider)
            self.ids.emotion_box.add_widget(emotion_layout)

    def confirm(self, instance):
        db = DBHelper()
        db.save_feedback(True)
        db.close()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'offer_skill'

    def adjust(self, instance):
        db = DBHelper()
        db.save_feedback(False)
        db.close()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'adjust_emotion'
