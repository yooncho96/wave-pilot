from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.lang import Builder
import os

from data.db_helper import DBHelper

class AdjustEmotionScreen(Screen):
    """
    1) Apologize
    2) Present all top 3 emotions, each with a sliding scale (0-10) displaying analysis results,
       and ask to adjust accordingly.
       Include another option "Other"
    3) If "other" chosen, show multiple choice of all emotion names
       When chosen, show sliding scale (0-10)
    """
    def __init__(self, **kwargs):
        super(AdjustEmotionScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'adjust_emotion.kv')
        Builder.load_file(kv_path)
        self.display_emotions()

    def display_emotions(self):
        self.ids.message_label.text = (
            "We apologize. Can you help us get to know you better?\n"
            "Please choose the emotion that is closest to what you feel.\n"
            "You can correct the rating if you wish."
        )

        db = DBHelper()
        emotion_data = db.get_emotion_data()
        db.close()

        sorted_emotions = sorted(emotion_data.items(), key=lambda x: x[1], reverse=True)
        top3_emotions = sorted_emotions[:3]

        for emotion, value in top3_emotions:
            emotion_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            emotion_label = Label(text=emotion, size_hint_x=0.5)
            emotion_slider = Slider(min=0, max=10, value=value, size_hint_x=0.5)
            emotion_layout.add_widget(emotion_label)
            emotion_layout.add_widget(emotion_slider)
            self.ids.emotion_box.add_widget(emotion_layout)

        other_btn = Button(text="Other", size_hint=(1, 0.1))
        other_btn.bind(on_release=self.show_other_emotions)
        self.ids.emotion_box.add_widget(other_btn)

    def show_other_emotions(self, instance):
        self.ids.emotion_box.clear_widgets()
        db = DBHelper()
        emotion_data = db.get_emotion_data()
        db.close()

        for emotion in emotion_data.keys():
            emotion_btn = Button(text=emotion)
            emotion_btn.bind(on_release=self.select_emotion)
            self.ids.emotion_box.add_widget(emotion_btn)

    def select_emotion(self, instance):
        self.ids.emotion_box.clear_widgets()
        selected_emotion = instance.text

        self.ids.emotion_box.add_widget(Label(text=f"How strong is {selected_emotion} right now?", font_size='16sp'))
        slider = Slider(min=0, max=10, value=0)
        self.ids.emotion_box.add_widget(slider)

        next_button = Button(text="Next", size_hint=(1, 0.1))
        next_button.bind(on_release=lambda x: self.submit_emotion(selected_emotion, slider.value))
        self.ids.emotion_box.add_widget(next_button)

    def submit_emotion(self, emotion, value):
        db = DBHelper()
        db.adjust_emotion({emotion: round(value, 1)})
        db.close()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'offer_skill'
