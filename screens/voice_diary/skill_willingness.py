from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition

from data.db_helper import DBHelper

class OfferSkillScreen(Screen):
    
    def __init__(self, **kwargs):
        super(OfferSkillScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        message = f"""
            I'm so sorry you are feeling this way.\n
            And, I believe you can find a way to live with it.\n
            Would you like to give it a try?
            """
        self.layout.add_widget(Label(text=message))

        db = DBHelper()
        idx = db.get_current_idx()
        all_emotions = db.get_all_emotion_data()[idx]
        if all_emotions[12]:
            emotion, score = all_emotions[11].items()[0]
        else:
            adjusted = db.get_adjusted_main()
            emotion, score = adjusted.items()[0]

        try_btn = Button(text="Yes, I'll try", size_hint=(1, 0.1))
        if score > 7:
            try_btn.bind(on_release=self.go_distress_tolerance())
        elif score > 4 and score <= 7:
            try_btn.bind(on_release=self.go_check_the_facts())
        else:
            try_btn.bind(on_release=self.go_model_of_emotion())
        self.layout.add_widget(try_btn)

        later_btn = Button(text="Maybe later", size_hint=(1, 0.1))
        later_btn.bind(on_release=self.set_reminder())
        self.layout.add_widget(later_btn)

    def go_distress_tolerance(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screens/voice_diary/distress_tolerance/distress_tolerance"

    def go_check_the_facts(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screens/voice_diary/emotion_reg/check_the_facts"

    def go_model_of_emotion(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screens/voice_diary/emotion_reg/model_of_emotion"

    def set_reminder(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "screens/voice_diary/set_reminder"