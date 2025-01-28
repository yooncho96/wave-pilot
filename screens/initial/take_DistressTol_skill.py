from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data.db_helper import DBHelper
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class DistressTolScreen(Screen):
    def __init__(self, **kwargs):
        super(DistressTolScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text="Distress Tolerance", font_size=32, size_hint_y=None, height=50)
        layout.add_widget(title)
        
        description = Label(
            text="Next, can you pick some distress tolerance skills that work best for you?",
            size_hint_y=None, height=100
        )
        layout.add_widget(description)
        
        skills = ["TIPP skills", "STOP", "Self-soothing", "Pros and cons","Something else"]
        for skill in skills:
            btn = Button(text=skill, size_hint_y=None, height=50)
            btn.bind(on_release=self.action)
            layout.add_widget(btn)

        self.next_button = Button(text="Next", size_hint_y=None, height=50)
        self.next_button.bind(on_release=self.go_next)
        
        self.add_widget(layout)

        self.selected_list = []
    
    def action(self, instance):
        if instance.text == "TIPP skills":
            title = "TIPP skills for you to choose from:"
            layout = BoxLayout(orientation="vertical")
            for skill in ["Temperature - Ice diving", "Intense exercise", "Paced breathing", "Progressive muscle relaxation"]:
                btn = Button(text=skill, size_hint_y=None, height=50)
                btn.bind(on_release=self.change(skill))
                layout.add_widget(btn)
            done_btn = Button(text="Done", size_hint_y= None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            layout.add_widget(done_btn)
            popup = Popup(title=title, content=layout)
            action = popup.open()

        elif instance.text == "STOP":
            action = self.change(instance.text)

        elif instance.text == "Self-soothing":
            title = "What soothes your senses most?"
            layout = BoxLayout(orientation="vertical")
            for sense in ["Sight","Sound","Touch","Smell","Taste"]:
                text_input = TextInput(hint_text=sense, size_hint_y=None, height=50)
                layout.add_widget(text_input)

            done_btn = Button(text="Done", size_hint_y= None, width=100)
            def input_complete(instance):
                input_list = [x.text for x in layout.children[:-1]] 
                popup.dismiss()
            done_btn.bind(on_release=input_complete())
            layout.add_widget(done_btn)

            popup = Popup(title=title, content=layout)
            action = popup.open()

        elif instance.text == "Pros and Cons":
            action = self.change(instance.text)

        elif instance.text == "Something else":
            action = self.other()
        
        return action

    def change(self, instance, skill):
        if instance.background_color == [0.39, 0.58, 0.93, 1]:  # Light cornflower blue = was selected before
            instance.background_color = [1, 1, 1, 1]  # Reset to white = unselect
        else:       # was not selected before
            instance.background_color = [0.39, 0.58, 0.93, 1]  # Light cornflower blue = select

        if skill == "Something else in mind?":
            # Open a popup with a text input for the user to enter their own skill
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            text_input = TextInput(hint_text="Tell us here", size_hint_y=None, height=50)
            box.add_widget(text_input)
            submit_btn = Button(text="Submit", size_hint_y=None, width=100)
            submit_btn.bind(on_release=lambda btn: (self.add_skill(text_input.text), popup.dismiss()))
            box.add_widget(submit_btn)

            popup = Popup(title="We always love additions to our list.",
                  content=box,
                  size_hint=(0.8, 0.3))
            popup.open()
        else:
            self.add_skill(skill)

    def add_skill(self, skill):
        if isinstance(skill, str):
            self.selected_list.append(skill)
        elif isinstance(skill, list):
            self.selected_list.extend(skill)

    def go_next(self, instance):
        if len(self.selected_list) >= 3:
            db = DBHelper()
            db.create_distress_tolerance_table()
            db.set_preferred_distress_tolerance(self.selected_list)
            db.close()
            self.manager.current = "take_DistressTol_skill"
        else:
            done_btn = Button(text="Done", size_hint_y= None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            popup = Popup(title="Please select at least three skills.",
                          content=done_btn,
                          size_hint=(0.8, 0.3))
