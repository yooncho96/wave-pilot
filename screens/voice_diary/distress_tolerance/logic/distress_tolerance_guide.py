from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import os

from data.db_helper import DBHelper
from functions.make_boxes import BorderedLabel, BorderedTextInput
from functions.timer import Timer
from screens.voice_diary.distress_tolerance.logic.descriptions_practice import description_list, STOP, SelfSoothing, Pros_and_Cons, Other
from typing import Union

skills_dict = {
    "TIPP_skills_Temperature_Ice_diving": "Ice diving", 
    "TIPP_skills_Intense_exercise": "Intense exercise", 
    "TIPP_skills_Paced_breathing": "Paced breathing",
    "TIPP_skills_Progressive_muscle_relaxation": "Progressive muscle relaxation",
    "STOP": "STOP",
    "Pros_and_Cons": "Pros and Cons"
}

class DistressToleranceGuideScreen(Screen):

    def __init__(self, skill_label: Label, **kwargs):
        super(DistressToleranceGuideScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'distress_tolerance_guide.kv')
        Builder.load_file(kv_path)
        self.skill_label = skill_label

    def next_screen(self, instance):
        self.manager.transition = FadeTransition(duration=1)
        if self.skill_label.text in skills_dict.values():
            skill_key = list(skills_dict.keys())[list(skills_dict.values()).index(self.skill_label.text)]
            self.idv_layouts(description_list.get(skill_key))
        elif self.skill_label.text.startswith("Soothing"):
            self.idv_layouts(SelfSoothing)
        else:
            self.idv_layouts(Other)

    def idv_layouts(self, description: Union[str, list]):
        self.ids.content_box.clear_widgets()

        title_label = Label(text=self.skill_label.text, bold=True, font_size='20sp')
        self.ids.content_box.add_widget(title_label)

        if description == STOP:
            self.stop_index = 0
            self.update_stop_layout()
        else: 
            self.ids.content_box.add_widget(Label(text=description))
            if description == Pros_and_Cons:
                self.ids.content_box.add_widget(self.make_table())
            else:
                if description != Other:
                    self.ids.content_box.add_widget(Label(text="Let's try this for a couple of minutes."))
                self.ids.content_box.add_widget(Timer(time_in_minutes=3))

        done_btn = Button(text="All done")
        done_btn.bind(on_release=self.done)
        self.ids.content_box.add_widget(done_btn)

    def update_stop_layout(self):
        self.ids.content_box.clear_widgets()
        if self.stop_index < len(STOP):
            stop_letter = Label(text="STOP"[self.stop_index], bold=True)
            stop_label = Label(text=STOP[self.stop_index])
            next_button = Button(text="Next", size_hint=(1, 0.2))
            next_button.bind(on_release=self.next_stop)
            self.ids.content_box.add_widget(stop_letter)
            self.ids.content_box.add_widget(stop_label)
            self.ids.content_box.add_widget(next_button)

    def next_stop(self, instance):
        self.stop_index += 1
        self.manager.transition = FadeTransition(duration=1)
        if self.stop_index == len(STOP):
            self.done(instance)
        else:
            self.update_stop_layout()

    def make_table(self):
        table_layout = GridLayout(cols=3, rows=3, spacing=2, size_hint=(None, None))
        table_layout.bind(minimum_size=table_layout.setter("size"))

        table_layout.add_widget(BorderedLabel(text="", size_hint=(None, None), size=(100, 100), thick_border=True))
        table_layout.add_widget(BorderedLabel(text="Pros", size_hint=(None, None), size=(100, 100), thick_border=True))
        table_layout.add_widget(BorderedLabel(text="Cons", size_hint=(None, None), size=(100, 100), thick_border=True))

        table_layout.add_widget(BorderedLabel(text="Acting on (...)"))
        table_layout.add_widget(BorderedTextInput(key="act_pros", parent_screen=self))
        table_layout.add_widget(BorderedTextInput(key="act_cons", parent_screen=self))

        table_layout.add_widget(BorderedLabel(text="Not acting on (...)"))
        table_layout.add_widget(BorderedTextInput(key="not_pros", parent_screen=self))
        table_layout.add_widget(BorderedTextInput(key="not_cons", parent_screen=self))

        return table_layout

    def done(self, instance):
        self.manager.current = 'after_emotion_rate'
