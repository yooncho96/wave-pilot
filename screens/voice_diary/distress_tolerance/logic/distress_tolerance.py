from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os
import random

from data.db_helper import DBHelper

skills_dict = {
    "TIPP_skills_Temperature_Ice_diving": "Ice diving", 
    "TIPP_skills_Intense_exercise": "Intense exercise", 
    "TIPP_skills_Paced_breathing": "Paced breathing",
    "TIPP_skills_Progressive_muscle_relaxation": "Progressive muscle relaxation",
    "STOP": "STOP",
    "SelfSoothing_Sight": "Soothing your sense of sight",
    "SelfSoothing_Sound": "Soothing your sense of sound",
    "SelfSoothing_Touch": "Soothing your sense of touch",
    "SelfSoothing_Smell": "Soothing your sense of smell",
    "SelfSoothing_Taste": "Soothing your sense of taste",
    "Pros_and_Cons": "Pros and Cons"
}

class DistressTolerancePracticeScreen(Screen):
    """
    Pulls up a random stored skill from DBHelper.
    User can choose Yes, Cannot, or No.
    If No, decrease future probability of suggesting that skill.
    """
    def __init__(self, **kwargs):
        super(DistressTolerancePracticeScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'distress_tolerance_practice.kv')
        Builder.load_file(kv_path)

        db = DBHelper()
        emotion, score = db.get_final_key_emotion()
        selected_dict = db.get_distress_tolerance()
        db.create_DistTol_prob_table()
        self.prob_dict = db.get_DistTol_probs()
        db.close()

        self.skills_list = []
        self.preserve_names = {}

        for key, value in selected_dict.items():
            if isinstance(value, str):
                skill_values = value.split(',')
                for skill_value in skill_values:
                    txt = f"{skills_dict.get(key.replace('Details_', ''), key)}: {skill_value.strip()}"
                    self.skills_list.append(txt)
                    self.preserve_names[txt] = f"{key.replace('Details_', '')}_{skill_value.strip()}"
            elif key in skills_dict:
                self.skills_list.append(skills_dict[key])
                self.preserve_names[skills_dict[key]] = key
            else:
                cleaned_key = key.replace('_', '')[6:]
                self.skills_list.append(cleaned_key)
                self.preserve_names[cleaned_key] = key

        self.swipe_dict = {name: None for name in self.preserve_names.values()}
        self.rounds = 0
        self.i = 0
        self.done = False

    def display_skills(self):
        if self.i == 0:
            self.random_order = random.choices(self.skills_list, weights=[self.prob_dict[skill] for skill in self.skills_list])
        self.ids.skill_label.text = self.random_order[self.i]

    def on_touch_move(self, touch):
        db_name = self.preserve_names[self.ids.skill_label.text]
        if touch.dx < -40:  # Swipe left
            self.swipe_dict[db_name] = "Dislike"
            self.i += 1
            if self.i >= len(self.skills_list):
                self.end_of_list()
            else:
                self.display_skills()
        elif touch.dx > 40:  # Swipe right
            self.swipe_dict[db_name] = "Like"
            self.chose_skill()
        elif touch.dy < -40:  # Swipe down
            self.swipe_dict[db_name] = "Cannot"

    def end_of_list(self):
        self.rounds += 1
        if self.rounds == 1:
            self.prompt_try_again()
        elif self.rounds == 2:
            self.prompt_contact()

    def prompt_try_again(self):
        popup = Popup(title="Not Interested?",
                      content=Label(text="Can you try to choose one to practice for us?"),
                      size_hint=(0.8, 0.4))
        popup.open()

    def prompt_contact(self):
        popup = Popup(title="Need Help?",
                      content=Label(text="Would you like to call a trusted contact instead?"),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_contacts(self):
        self.manager.current = 'crisis'

    def random_skill(self):
        db = DBHelper()
        db.update_prob(self.swipe_dict)
        current_probs = db.get_DistTol_probs()
        db.close()
        random_skill = random.choices(self.skills_list, weights=[current_probs[self.preserve_names[skill]] for skill in self.skills_list])[0]
        self.manager.current = 'distress_tolerance_guide'
        self.manager.get_screen('distress_tolerance_guide').set_skill(random_skill)

    def chose_skill(self):
        db = DBHelper()
        db.update_prob(self.swipe_dict)
        db.close()
        self.manager.current = 'distress_tolerance_guide'
        self.manager.get_screen('distress_tolerance_guide').set_skill(self.ids.skill_label.text)
