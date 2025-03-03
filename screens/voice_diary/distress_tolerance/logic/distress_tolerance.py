from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup

from kivy.lang import Builder
import random
import os

from data.skills_db_Helper import DBHelper

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

class DistressToleranceScreen(Screen):
    """
    Pulls up a random stored skills from DBHelper.
    User can choose Yes, Cannot, or No
    If No, decrease future probability of suggesting that skill
    """
    def __init__(self, **kwargs):
        super(DistressToleranceScreen, self).__init__(**kwargs)
        
        db = DBHelper()
        emotion, score = db.get_final_key_emotion()
        selected_dict = db.get_distress_tolerance()
        db.create_DistTol_prob_table()
        self.prob_dict = db.get_DistTol_probs()
        db.close()

        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'distress_tolerance_notice.kv')
        Builder.load_file(kv_path)

        intro = f"""
            Your {emotion} is at a {score} out of 10.\n
            When emotions rise and start to get overwhelming,\n
            it helps to teach our body and mind how to tolerate it\n
            until it gets a little toned down.\n
            And don't worry, because no one can stay {emotion} forever.
            """
        self.ids.message_label.text = intro

        self.skills_list=[]
        self.preserve_names={}
        for key, value in selected_dict.items():
            if isinstance(value, str):
                skill_values = value.split(',')
                for skill_value in skill_values:
                    txt=f"{skills_dict[key.replace("Details_", "")]}: {skill_value.strip()}"
                    self.skills_list.append(txt)
                    self.preserve_names[txt] = f"{key.replace("Details_", "")}_{skill_value}"
            elif key in skills_dict.keys():
                self.skills_list.append(skills_dict[key])
                self.preserve_names[skills_dict[key]] = key
            else:
                self.skills_list.append(key.replace("_","")[6:])
                self.preserve_names[key.replace("_","")[6:]] = key

        self.swipe_dict = {name: None for name in self.preserve_names.values()}
        self.rounds=0
        self.i=0
        self.done=False

    def display_skills(self, instance):

        self.clear_widgets()
        self.ids.clear()
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'distress_tolerance_swipe.kv')
        Builder.load_file(kv_path)

        if self.i==0:
            self.random_order = random.choices(self.skills_list, weights=[self.prob_dict[skill] for skill in self.skills_list])
        self.ids.skill_label.text=self.random_order[self.i]

    def on_touch_move(self, touch):
        db_name = self.preserve_names[self.ids.skill_label.text]
        if touch.dx < -40:  # Swipe left
            if self.i==len(self.skills_list)-1:
                self.end_of_list()
                self.swipe_dict={}
                self.i=0
            else:
                self.swipe_dict[db_name]="Dislike"
                self.i+=1
                self.manager.transition.direction = 'left'
                self.manager.transition.duration = 0.5
                self.display_skills()
        elif touch.dx > 40:  # Swipe right
            self.swipe_dict[db_name]="Like"
            self.done=True
            self.chose_skill()
        elif touch.dy < -40:  # Swipe down
            self.swipe_dict[db_name]="Cannot"

    def end_of_list(self, instance):
        
        self.rounds+=1
        if self.rounds ==1:
            self.swipe_dict = {name: None for name in self.preserve_names.values()}
            title="Not up to it?"
            content = BoxLayout(orientation="vertical")
            content.add_widget(Label(text="""
                                        It looks like these skills aren't that appealing for you right now.\n
                                        At the same time, they are the skills you selected in your wise mind.\n
                                        Can you still try to choose one to practice for us?
                                        """
                                        ))
            ok_btn = Button(text="OK")
            ok_btn.bind(on_release=(popup.dismiss(), self.display_skills))
            content.add_widget(ok_btn)
        elif self.rounds==2:
            title = "We understand."
            content=BoxLayout(orientation="vertical")
            content.add_widget(Label(text="""
                                     It can be difficult to try out skills, and that's okay.
                                     Still, it worries us that you are in emotional distress for a while now.\n 
                                     Would you like to call a trusted contact instead?
                                     """
                                     ))
            contact_btn = Button(text="Yes, I would like to talk it out").bind(on_release=self.show_contacts)
            stay_btn = Button(text="That's okay, I'll just do a random skill").bind(on_release=self.random_skill)
            content.add_widget(contact_btn)
            content.add_widget(stay_btn)

        popup = Popup(title=title, content=content,
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def show_contacts(self, instance):
        self.swipe_dict = {name: None for name in self.preserve_names.values()}
        self.manager.current = 'crisis'

    def random_skill(self, instance):
        db=DBHelper()
        db.update_prob(self.swipe_dict)
        current=db.get_DistTol_probs()
        db.close()
        show_random = random.choices(self.skills_list, weights=[current[self.preserve_names[skill]] for skill in self.skills_list])[0]
        self.skill_label.text = show_random
        next_screen = self.manager.get_screen('distress_tolerance_guide')
        next_screen.get_skill(self.skill_label)

    def chose_skill(self):
        db=DBHelper()
        db.update_prob(self.swipe_dict)
        db.close()
        next_screen = self.manager.get_screen('distress_tolerance_guide')
        next_screen.get_skill(self.skill_label)
