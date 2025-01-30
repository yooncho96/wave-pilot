from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data.db_helper import DBHelper
from screens.initial.take_DistressTol_skill import DistressTolScreen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class MindfulnessScreen(Screen):
    def __init__(self, **kwargs):
        super(MindfulnessScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text="Mindfulness", font_size=32, size_hint_y=None, height=50)
        layout.add_widget(title)
        
        description = Label(
            text="We'd like to get a sense of what skills work best for you. Can you pick some of your favorite mindfulness skills from those listed below?",
            size_hint_y=None, height=100
        )
        layout.add_widget(description)
        
        skills = ["Breathing exercises", "Observe and Describe", "Participate", "Mediation and self-reflection","Something else"]
        for skill in skills:
            btn = Button(text=skill, size_hint_y=None, height=50)
            btn.bind(on_release=self.show_dropdown)
            layout.add_widget(btn)

        self.next_button = Button(text="Next", size_hint_y=None, height=50)
        self.next_button.bind(on_release=self.go_next)
        
        self.add_widget(layout)

        self.selected_list = []
    
    def show_dropdown(self, instance):
        dropdown = DropDown()
        
        if instance.text == "Breathing exercises":
            options = ["Paced breathing", "Box breathing", "Focusing on exhales", "Counting down from 10"]
        elif instance.text == "Observe and Describe":
            options = ["Narrate a task", "Blindfolded movement/taste", "Search for that color", "Search for that shape", "Learning from an animal friend", "5-4-3-2-1"]
        elif instance.text == "Participate":
            options = ["Coloring", "Doodling", "Taking a walk", "Cooking", "Dancing", "Puzzles", "Mindful eating"]
        elif instance.text == "Mediation and self-reflection":
            options = ["Light a candle", "Body Scan", "Set up mantras", "Journaling", "List of Gratitude"]
        elif instance.text == "Something else":
            options = ["Something else in mind?"]
        
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        
        dropdown.bind(on_select=lambda instance, x: self.change(instance, x, instance.text))
        self.dropdown = dropdown

    def add_tag(self, skill):
        # Create a tag for the selected option
        tag_layout = BoxLayout(orientation="horizontal",size_hint_y=None, height=30)
        tag_label = Label(text=skill, color=(0, 0, 1, 1), size_hint_x=None, width=200)
        remove_btn = Button(text='X', size_hint_x=None, width=30)
        
        remove_btn.bind(on_release=lambda btn: self.remove_tag(tag_layout, skill))
        
        tag_layout.add_widget(tag_label)
        tag_layout.add_widget(remove_btn)
        
        if not hasattr(self, 'tag_box'):
            self.tag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            self.add_widget(self.tag_box, index=1)  # Add the tag box layout under the title

        self.tag_box.add_widget(tag_layout)

    def change(self, instance, skill):
        if instance.background_color == [0.39, 0.58, 0.93, 1]:  # Light cornflower blue = was selected before
            instance.background_color = [1, 1, 1, 1]  # Reset to white = unselect
            for child in self.tag_box.children[:]:
                if isinstance(child, BoxLayout) and child.children[1].text == skill:
                    self.tag_box.remove_widget(child)
        else:       # was not selected before
            instance.background_color = [0.39, 0.58, 0.93, 1]  # Light cornflower blue = select

        if skill == "Something else in mind?":
            # Open a popup with a text input for the user to enter their own skill
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            text_input = TextInput(hint_text="Tell us here", size_hint_y=None, height=50)
            box.add_widget(text_input)
            submit_btn = Button(text="Submit", size_hint_y=None, width=100)
            submit_btn.bind(on_release=lambda btn: (self.add_tag(text_input.text), popup.dismiss()))
            box.add_widget(submit_btn)

            popup = Popup(title="We always love additions to our list.",
                  content=box,
                  size_hint=(0.8, 0.3))
            popup.open()
        else:
            self.selected_list.append(skill.replace(" ", "_"))
            self.add_tag(skill)

    def remove_tag(self, tag_layout, skill):
        self.remove_widget(tag_layout)
        self.selected_list.remove(skill.replace(" ", "_"))

    def go_next(self, instance):
        if len(self.selected_list) >= 3:
            db = DBHelper()
            db.create_mindfulness_table()
            db.set_preferred_mindfulness(self.selected_list)
            db.close()
            self.manager.current = DistressTolScreen
        else:
            done_btn = Button(text="Done", size_hint_y= None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            popup = Popup(title="Please select at least three skills.",
                          content=done_btn,
                          size_hint=(0.8, 0.3))
