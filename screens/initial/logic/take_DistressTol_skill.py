from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

from data.db_helper import DBHelper

class TakeDistressTolScreen(Screen):
    def __init__(self, **kwargs):
        super(TakeDistressTolScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'take_DistressTol_skill.kv')
        Builder.load_file(kv_path)

        self.selected_list = []
        self.detail_list = ["Sight", "Sound", "Touch", "Smell", "Taste"]

    def action(self, instance):
        if instance.text == "Something else":
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
                        self.change(grandchild, f"{grandchild.text}", original_instance)
            popup.dismiss()
        submit_btn.bind(on_release=lambda _: submit(layout))
        popup_layout.add_widget(BoxLayout(size_hint_y=None, height=10))  # Spacer
        popup_layout.add_widget(submit_btn)

        popup = Popup(title="We always love additions to our list.",
                      content=popup_layout,
                      size_hint=(0.8, 0.3))
        popup.open()

    def change(self, instance, skill, original_instance):
        def toggle_color(instance):
            if instance.background_color == [0.39, 0.58, 0.93, 1]:
                instance.background_color = [1, 1, 1, 1]
            else:
                instance.background_color = [0.39, 0.58, 0.93, 1]

        toggle_color(original_instance)
        save_type = skill.replace(" - ", "_").replace(" ", "_")
        self.selected_list.append(save_type)

    def go_next(self, instance):
        if len(self.selected_list) >= 3:
            db = DBHelper()
            db.create_distress_tolerance_table()
            db.set_preferred_distress_tolerance(self.selected_list, self.detail_list)
            db.close()
            self.manager.current = 'TakeCrisisContact'
        else:
            popup = Popup(title="Please select at least three skills.",
                          content=Button(text="Done", size_hint_y=None, width=100, on_release=lambda x: popup.dismiss()),
                          size_hint=(0.8, 0.3))
            popup.open()
