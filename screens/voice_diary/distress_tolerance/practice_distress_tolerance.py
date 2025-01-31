from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from data.db_helper import DBHelper
from functions.make_boxes import BorderedLabel, BorderedTextInput
from functions.timer import Timer
from screens.voice_diary.distress_tolerance.descriptions_practice import description_list, STOP, SelfSoothing, Pros_and_Cons, Other
from screens.voice_diary.after_emotion_rate import AfterEmotionScreen
from screens.crisis import CrisisScreen

from kivy.uix.popup import Popup
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

    def __init__(self, skill_label: Label, **kw):
        super(DistressToleranceGuideScreen, self).__init__(**kw)
        self.skill_label = skill_label
        self.layout=BoxLayout(orientation="vertical")

        encouragement = Label(text="You're showing real courage and allowing yourself the self-care you deserve.")
        next_button = Button(text="Next", size_hint=(1, 0.2))
        next_button.bind(on_release=self.next_screen)
        self.layout.add_widget(encouragement)
        self.layout.add_widget(next_button)
        self.add_widget(self.layout)

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
        
        layout = BoxLayout(orientation="vertical")
        
        title_label = self.skill_label
        title_label.bold = True
        title_label.font_size = '20sp'
        layout.add_widget(title_label)

        if description == STOP:
            self.stop_index = 0
            self.stop_layout = layout
            self.update_stop_layout()

        else: 
            layout.add_widget(Label(text=description))
            if description == Pros_and_Cons:
                self.input_values = {
                    "act_pros": "",
                    "act_cons": "",
                    "not_pros": "",
                    "not_cons": ""
                }
                layout.add_widget(self.make_table())

            else:
                if description != Other:
                    layout.add_widget(Label(text="Let's try this for a couple of minutes."))
                layout.add_widget(Timer(time_in_minutes=3))
        done_btn = Button(text="All done")
        done_btn.bind(self.done)
        layout.add_widget(done_btn)

        self.clear_widgets()
        self.add_widget(layout)

    def update_stop_layout(self):
        self.stop_layout.clear_widgets()
        stop = "STOP"
        if self.stop_index < len(STOP):
            stop_letter = Label(text=stop[self.stop_index], bold=True)
            stop_label = Label(text=STOP[self.stop_index])
            next_button = Button(text="Next", size_hint=(1, 0.2))
            next_button.bind(on_release=self.next_stop)
            self.stop_layout.add_widget(stop_letter)
            self.stop_layout.add_widget(stop_label)
            self.stop_layout.add_widget(next_button)

    def next_stop(self, instance):
        self.stop_index += 1
        self.manager.transition = FadeTransition(duration=1)
        if self.stop_index ==len(STOP):
            self.done()
        else:
            self.update_stop_layout()

    def make_table(self):
        # Table Layout (Grid)
        table_layout = GridLayout(cols=3, rows=3, spacing=2, size_hint=(None, None))
        table_layout.bind(minimum_size=table_layout.setter("size"))

        # Header Row
        table_layout.add_widget(BorderedLabel(text="", size_hint=(None, None), size=(100, 100), thick_border=True))  # Empty Top-Left Cell
        table_layout.add_widget(BorderedLabel(text="Pros", size_hint=(None, None), size=(100, 100), thick_border=True))
        table_layout.add_widget(BorderedLabel(text="Cons", size_hint=(None, None), size=(100, 100), thick_border=True))

        # Row 1 (Acting on)
        table_layout.add_widget(BorderedLabel(text="Acting on (...)", size_hint=(None, None), size=(100, 100), thick_border=True))
        table_layout.add_widget(BorderedTextInput(key="act_pros", parent_screen=self, size_hint=(None, None), size=(100, 100)))
        table_layout.add_widget(BorderedTextInput(key="act_cons", parent_screen=self, size_hint=(None, None), size=(100, 100)))

        # Row 2 (Not Acting on)
        table_layout.add_widget(BorderedLabel(text="Not acting on (...)", size_hint=(None, None), size=(100, 100), thick_border=True))
        table_layout.add_widget(BorderedTextInput(key="not_pros", parent_screen=self, size_hint=(None, None), size=(100, 100)))
        table_layout.add_widget(BorderedTextInput(key="not_cons", parent_screen=self, size_hint=(None, None), size=(100, 100)))

        return table_layout

    def done(self):
        self.manager.current = AfterEmotionScreen