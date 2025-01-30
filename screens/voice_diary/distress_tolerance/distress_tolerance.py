from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data.db_helper import DBHelper

from screens.crisis import CrisisScreen
from screens.voice_diary.after_emotion_rate import AfterEmotionRateScreen
from screens.voice_diary.emotion_reg.check_the_facts import ChecktheFactsScreen

from kivy.uix.popup import Popup
import random

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
    Pulls up a random stored skills from DBHelper.
    User can choose Yes, Cannot, or No
    If No, decrease future probability of suggesting that skill
    """
    def __init__(self, **kwargs):
        super(DistressTolerancePracticeScreen, self).__init__(**kwargs)
        
        db = DBHelper()
        emotion, score = db.get_final_key_emotion()
        skills_list = [key for key, value in db.get_distress_tolerance().items if value]
        db.close()

        self.layout = BoxLayout(orientation='vertical')
        title = Label(text="Distress Tolerance")
        intro = f"""
            Your {emotion} is at a {score} out of 10.\n
            When emotions rise and start to get overwhelming,\n
            it helps to teach our body and mind how to tolerate it\n
            until it gets a little toned down.\n
            And don't worry, because no one can stay {emotion} forever.
            """
        self.layout.add_widget(Label(text=intro))

        self.skill_names = []
        for skill in skills_list:
            if skill in skills_dict.keys():
                skill_name = skills_dict[skill]
            else:
                skill_name = skill.replace("_", " ")[6:]
            self.skill_names.append(skill_name)

        random_skill = random.choice(self.skill_names)
        ##############################################