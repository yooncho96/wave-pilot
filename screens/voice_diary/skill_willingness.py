from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition

from data.db_helper import DBHelper
# from screens.voice_diary.assess_emotion.confirm_emotion import tries
from screens.voice_diary.distress_tolerance.distress_tolerance import DistressTolerancePracticeScreen
from screens.voice_diary.emotion_reg.check_the_facts import CheckTheFactsScreen
from screens.voice_diary.emotion_reg.model_of_emotion import ModelofEmotionScreen
from screens.voice_diary.set_reminder import SetReminderScreen

class OfferSkillScreen(Screen):
    
    def __init__(self, reminded=False, **kwargs):
        super(OfferSkillScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        if reminded:
            message = f"""
                We're so glad you came back on our reminder.\n
                Are you ready?
                """
            yes_txt = "Yes, I'm ready"
            no_txt = "I need a little more time"
        else:
            message = f"""
                We're so sorry you are feeling this way.\n
                And, we believe you can find a way to live with it.\n
                Would you like to give it a try?
                """
            yes_txt = "Sure, why not"
            no_txt = "Maybe later"
        self.layout.add_widget(Label(text=message))

        db = DBHelper()
        emotion, score = db.get_final_key_emotion()

        try_btn = Button(text=yes_txt, size_hint=(1, 0.1))
        if score > 7:
            try_btn.bind(on_release=self.go_next(DistressTolerancePracticeScreen))
        elif score > 4 and score <= 7:
            try_btn.bind(on_release=self.go_next(CheckTheFactsScreen))
        else:
            try_btn.bind(on_release=self.go_next(ModelofEmotionScreen))
        self.layout.add_widget(try_btn)

        later_btn = Button(text=no_txt, size_hint=(1, 0.1))
        later_btn.bind(on_release=self.go_next(SetReminderScreen))
        self.layout.add_widget(later_btn)

    def go_next(self, instance, screen):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screen