from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from data.db_helper import DBHelper

import json

class UpdateMindfulness(Screen):
    def __init__(self, **kwargs):
        super(UpdateMindfulness, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'update_mindfulness_skill.kv')
        Builder.load_file(kv_path)

        db = DBHelper()
        self.past_selections = db.get_mindfulness()
        db.close()

        self.selected_list = []
        for key, value in self.past_selections.items():
            if value:
                self.add_tag(key)
                self.selected_list.append(key)

    def add_tag(self, skill):
        tag_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        tag_label = self.ids.tag_box.add_widget(Button(text=skill, size_hint_x=None, width=200))
        remove_btn = Button(text='X', size_hint_x=None, width=30)

        remove_btn.bind(on_release=lambda btn: self.remove_tag(tag_layout, skill))
        tag_layout.add_widget(tag_label)
        tag_layout.add_widget(remove_btn)
        self.ids.tag_box.add_widget(tag_layout)

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
            options = [x.replace('Other_', '') for x in self.past_selections if 'Other_' in x] + ['Something else in mind?']

        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            if option.replace(" ", "_") in self.past_selections.keys():
                btn.background_color = (0.39, 0.58, 0.93, 1)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        dropdown.bind(on_select=lambda instance, x: self.change(instance, x, instance.text))
        dropdown.open(instance)

    def change(self, instance, skill):
        if instance.background_color == [0.39, 0.58, 0.93, 1]:
            instance.background_color = [1, 1, 1, 1]
            self.selected_list.remove(skill.replace(" ", "_"))
            for child in self.ids.tag_box.children[:]:
                if isinstance(child, BoxLayout) and child.children[1].text == skill:
                    self.ids.tag_box.remove_widget(child)
        else:
            instance.background_color = [0.39, 0.58, 0.93, 1]
            self.selected_list.append(skill.replace(" ", "_"))
            self.add_tag(skill)

        if skill == "Something else in mind?":
            self.show_custom_input(instance)

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
                        self.selected_list.append(grandchild.text)
            popup.dismiss()
        submit_btn.bind(on_release=lambda _: submit(layout))
        popup_layout.add_widget(BoxLayout(size_hint_y=None, height=10))
        popup_layout.add_widget(submit_btn)

        popup = Popup(title="We always love additions to our list.", content=popup_layout, size_hint=(0.8, 0.3))
        popup.open()

    def remove_tag(self, tag_layout, skill):
        self.ids.tag_box.remove_widget(tag_layout)
        self.selected_list.remove(skill.replace(" ", "_"))

    def go_next(self, instance):
        if len(self.selected_list) >= 3:
            db = DBHelper()
            db.set_preferred_mindfulness(self.selected_list)
            db.close()

            done_btn = Button(text="Done", size_hint_y=None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            popup = Popup(title="I'll keep your selections in mind!", content=done_btn, size_hint=(0.8, 0.3))

            self.manager.current = self.manager.previous()
        else:
            done_btn = Button(text="Done", size_hint_y=None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            popup = Popup(title="Please select at least three skills.", content=done_btn, size_hint=(0.8, 0.3))
