from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

from data.db_helper import DBHelper

class TakeMindfulnessScreen(Screen):
    def __init__(self, **kwargs):
        super(TakeMindfulnessScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'take_mindfulness_skill.kv')
        Builder.load_file(kv_path)

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
        dropdown.open(instance)

    def add_tag(self, skill):
        tag_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        tag_label = Label(text=skill, color=(0, 0, 1, 1), size_hint_x=None, width=200)
        remove_btn = Button(text='X', size_hint_x=None, width=30)
        
        remove_btn.bind(on_release=lambda btn: self.remove_tag(tag_layout, skill))
        
        tag_layout.add_widget(tag_label)
        tag_layout.add_widget(remove_btn)
        
        if not hasattr(self, 'tag_box'):
            self.tag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            self.add_widget(self.tag_box, index=1)

        self.tag_box.add_widget(tag_layout)

    def change(self, instance, skill):
        if instance.background_color == [0.39, 0.58, 0.93, 1]:
            instance.background_color = [1, 1, 1, 1]
            for child in self.tag_box.children[:]:
                if isinstance(child, BoxLayout) and child.children[1].text == skill:
                    self.tag_box.remove_widget(child)
        else:
            instance.background_color = [0.39, 0.58, 0.93, 1]

        if skill == "Something else in mind?":
            self.show_custom_input(instance)
        else:
            self.selected_list.append(skill.replace(" ", "_"))
            self.add_tag(skill)

    def show_custom_input(self, original_instance):
        popup_layout = BoxLayout(orientation='vertical')

        layout = BoxLayout(orientation='vertical')

        def add_more(layout):
            new_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            layout.add_widget(new_box)

            input_field = TextInput(hint_text="Tell us here", size_hint_y=None, height=50)
            new_box.add_widget(input_field)

            more_btn = Button(text="+", size_hint_y=None, width=50, disabled=True)
            more_btn.bind(on_release=lambda _: add_more(layout))
            new_box.add_widget(more_btn)

            def delete(box):
                layout.remove_widget(box)
                if len(layout.children) == 1:
                    add_more(layout)
            del_btn = Button(text="—", size_hint_y=None, width=50, disabled=True)
            del_btn.bind(on_release=lambda _: delete(new_box))
            new_box.add_widget(del_btn)

            def enable_buttons(*args):
                if input_field.text:
                    more_btn.disabled = False
                    del_btn.disabled = False
                else:
                    more_btn.disabled = True
                    del_btn.disabled = True
            input_field.bind(text=enable_buttons)

            layout.add_widget(new_box)
        
        add_more(layout)
        popup_layout.add_widget(layout)

        submit_btn = Button(text="Submit", size_hint_y=None, width=100)
        def submit(layout):
            for child in layout.children:
                for grandchild in child.children:
                    if isinstance(grandchild, TextInput):
                        self.add_tag(grandchild.text)
            popup.dismiss()
        submit_btn.bind(on_release=lambda _: submit(layout))
        popup_layout.add_widget(BoxLayout(size_hint_y=None, height=10))  # Spacer
        popup_layout.add_widget(submit_btn)

        popup = Popup(title="We always love additions to our list.",
                      content=popup_layout,
                      size_hint=(0.8, 0.3))
        popup.open()
    
    def remove_tag(self, tag_layout, skill):
        self.tag_box.remove_widget(tag_layout)
        self.selected_list.remove(skill.replace(" ", "_"))

    def go_next(self, instance):
        if len(self.selected_list) >= 3:
            db = DBHelper()
            db.create_mindfulness_table()
            db.set_preferred_mindfulness(self.selected_list)
            db.close()
            self.manager.current = 'TakeDistressTol'
        else:
            popup = Popup(title="Please select at least three skills.",
                          content=Button(text="Done", size_hint_y=None, width=100, on_release=lambda x: popup.dismiss()),
                          size_hint=(0.8, 0.3))
            popup.open()
