from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
import os
from data.diary_db_Helper import DBHelper

class OfferSkillScreen(Screen):
    def __init__(self, reminded=False, **kwargs):
        super(OfferSkillScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'offer_skill.kv')
        Builder.load_file(kv_path)

        self.reminded = reminded
        self.prepare_ui()

    def prepare_ui(self):
        self.ids.message_label.text = (
            "We're so glad you came back on our reminder.\nAre you ready?"
            if self.reminded
            else "We're so sorry you are feeling this way.\nAnd, we believe you can find a way to live with it.\nWould you like to give it a try?"
        )
        
        yes_txt = "Yes, I'm ready" if self.reminded else "Sure, why not"
        no_txt = "I need a little more time" if self.reminded else "Maybe later"

        self.ids.try_button.text = yes_txt
        self.ids.later_button.text = no_txt

        db = DBHelper()
        emotion, score = db.get_final_key_emotion()

        if score > 7:
            self.ids.try_button.bind(on_release=lambda instance: self.go_next('distress_tolerance'))
        elif score > 4:
            self.ids.try_button.bind(on_release=lambda instance: self.go_next('check_the_facts'))
        else:
            self.ids.try_button.bind(on_release=lambda instance: self.go_next('model_of_emotion'))

        self.ids.later_button.bind(on_release=lambda instance: self.go_next('set_reminder'))

    def go_next(self, screen_name):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screen_name