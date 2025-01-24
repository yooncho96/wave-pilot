# screens/emotion_data.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from data.db_helper import DBHelper
from data.db_helper import emotion_list

class ConfirmEmotionScreen (Screen):

    def __init__(self, **kwargs):
        super(ConfirmEmotionScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

    def confirm(self, instance):
        db = DBHelper()
        first_try = db.get_emotion_data()
        db.close()

        sorted_emotions = [x for x in first_try.keys()]

        message = f"""
            I sense these emotions in your voice diary.\n
            Let me know if you feel a bit differently.
            """
        self.layout.add_widget(Label(text=message))

        top3_emotions = {
            sorted_emotions[0]: first_try[sorted_emotions[0]],
            sorted_emotions[1]: first_try[sorted_emotions[1]],
            sorted_emotions[2]: first_try[sorted_emotions[2]]
        }
        for emotion, value in top3_emotions.items():
            emotion_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            emotion_label = Label(text=emotion, size_hint_x=0.5)
            emotion_slider = Slider(min=0, max=10, value=value, size_hint_x=0.5)
            emotion_layout.add_widget(emotion_label)
            emotion_layout.add_widget(emotion_slider)
            self.layout.add_widget(emotion_layout)

        # Buttons to confirm or deny emotion
        confirm_btn = Button(text="Confirm", size_hint=(1, 0.1))
        confirm_btn.bind(on_release=self.next())
        self.layout.add_widget(confirm_btn)

        deny_btn = Button(text="Deny", size_hint=(1, 0.1))
        deny_btn.bind(on_release=self.adjust())
        self.layout.add_widget(deny_btn)

    def next(self, instance):
        db = DBHelper()
        db.save_feedback(True)
        db.close()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screens/voice_diary/skill_willingness"
        
    def adjust(self, instance):
        db = DBHelper()
        db.save_feedback(False)
        db.close()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screens/voice_diary/adjust_emotion"