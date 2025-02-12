from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

from data.skills_db_Helper import DBHelper

class TakeDistressTolScreen(Screen):
    def __init__(self, **kwargs):
        super(TakeDistressTolScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'take_DistressTol_skill.kv')
        Builder.load_file(kv_path)

        self.selected_list = []
        self.detail_list = ["Sight", "Sound", "Touch", "Smell", "Taste"]

    def tipp_action(self, instance):
        title = "TIPP skills for you to choose from:"
        layout = BoxLayout(orientation="vertical")
        for skill in ["Temperature - Ice diving", "Intense exercise", "Paced breathing", "Progressive muscle relaxation"]:
            btn = Button(text=skill, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn_instance: self.change(btn_instance, skill, instance))
            layout.add_widget(btn)
        done_btn = Button(text="Done", size_hint_y= None, width=100)
        done_btn.bind(on_release=popup.dismiss())
        layout.add_widget(done_btn)
        popup = Popup(title=title, content=layout)
        popup.open()

    def soothing_action(self, instance):
        title = "What soothes your senses the most?"

        def replace_widget(instance, sense):
            if isinstance(instance, TextInput):
                replacement = Button(text=sense, size_hint_y=None, height=50)
            elif isinstance(instance, Button):
                replacement = TextInput(hint_text=sense, size_hint_y=None, height=50)
            layout.remove_widget(instance)
            layout.add_widget(replacement)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="You can list multiple methods separated with commas: a, b, ..."))
        for sense in ["Sight","Sound","Touch","Smell","Taste"]:
            btn = Button(text=sense, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn_instance: replace_widget(btn_instance, sense))
            layout.add_widget(btn)
        
        def on_touch_down(instance, touch):
            if not instance.collide_point(*touch.pos):
                for child in layout.children:
                    if isinstance(child, TextInput) and not child.text:
                        replace_widget(child, child.hint_text)
            return super(TakeDistressTolScreen, self).on_touch_down(touch)

        self.bind(on_touch_down=on_touch_down)
            
        done_btn = Button(text="Done", size_hint_y= None, width=100)
        def input_complete(instance):   # input complete, iterate textbox and process self.change for each
            for child in layout.children:
                if isinstance(child, TextInput):
                    self.change(child, child.text, instance)
            popup.dismiss()
        done_btn.bind(on_release=input_complete)
        layout.add_widget(done_btn)

        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_custom_input(self, instance):
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
                        self.change(grandchild, f"{grandchild.text}", instance)
            popup.dismiss()
        submit_btn.bind(on_release=lambda _: submit(layout))
        popup_layout.add_widget(BoxLayout(size_hint_y=None, height=10))  # Spacer
        popup_layout.add_widget(submit_btn)

        popup = Popup(title="We always love additions to our list.",
                      content=popup_layout,
                      size_hint=(0.8, 0.3))
        popup.open()

    def change(self, instance, skill, original_instance):
        
        if original_instance.text in ["TIPP skills", "Self-soothing"]:     # instance = button, text input
            if isinstance(instance, TextInput):
                save_type = f"SelfSoothing_{instance.hint_text}"
                for sense in self.detail_list:
                    if sense in save_type:
                        self.detail_list.replace(sense, skill)
            else:
                save_type = f"{original_instance.text}_{instance.text}"
            if any(x.background_color == [0.39, 0.58, 0.93, 1] for x in instance.parent.children):
                original_instance.background_color == [0.39, 0.58, 0.93, 1]
            else:
                original_instance.background_color = [1, 1, 1, 1]
        elif original_instance.text == "Something else":
            save_type = skill
        else:
            save_type = original_instance.text

        save_type = save_type.replace(" - ", "_")

        if instance.background_color == [0.39, 0.58, 0.93, 1]:  # Light cornflower blue = was selected before
            instance.background_color = [1, 1, 1, 1]  # Reset to white = unselect
            self.selected_list.remove(save_type.replace(" ","_"))
        else:       # was not selected before
            instance.background_color = [0.39, 0.58, 0.93, 1]  # Light cornflower blue = select
            self.selected_list.append(save_type.replace(" ","_"))

    def action(self, instance):
        self.change(instance, instance.text, instance)

    def go_next(self, instance):
        if len(self.selected_list) >= 3:
            db = DBHelper()
            db.create_distress_tolerance_table()
            db.set_preferred_distress_tolerance(self.selected_list, self.detail_list)
            db.close()
            self.manager.current = 'TakeCrisisContact'
        else:
            popup = Popup(title="Please select at least three skills.",
                          content=Button(text="Close", size_hint_y=None, width=100, on_release=lambda x: popup.dismiss()),
                          size_hint=(0.8, 0.3))
            popup.open()
