from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data.db_helper import DBHelper
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class UpdateDistressTol(Screen):
    def __init__(self, **kwargs):
        super(UpdateDistressTol, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text="Distress Tolerance", font_size=32, size_hint_y=None, height=50)
        layout.add_widget(title)
        
        description = Label(
            text="I hear you found something that works better for you!",
            size_hint_y=None, height=100
        )
        layout.add_widget(description)
        
        skills = ["TIPP skills", "STOP", "Self-soothing", "Pros and cons","Something else"]

        db = DBHelper()
        self.past_selections = db.get_distress_tolerance()
        db.close()

        self.selected_list = []
        self.detail_list=["Sight","Sound","Touch","Smell","Taste"]

        for skill in skills:
            btn = Button(text=skill, size_hint_y=None, height=50)
            btn.bind(on_release=self.action)
            layout.add_widget(btn)

            search_str = skill.replace(" " and "-", "_")
            if skill == "Something else":
                search_str = "Other"
            for key in self.past_selections.keys():
                if search_str in key:
                    btn.background_color = (0.39, 0.58, 0.93, 1)  # Light cornflower blue

        self.next_button = Button(text="Next", size_hint_y=None, height=50)
        self.next_button.bind(on_release=self.go_next)
        
        self.add_widget(layout)
    
    def action(self, instance):
        if instance.text == "TIPP skills":
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

        elif instance.text == "STOP":
            self.change(instance, instance.text, instance)

        elif instance.text == "Self-soothing":
            title = "What soothes your senses the most?"

            def replace_widget(instance, sense):
                if isinstance(instance, TextInput):
                    replacement = Button(text=sense, size_hint_y=None, height=50)
                elif isinstance(instance, Button):
                    replacement = TextInput(hint_text=sense, size_hint_y=None, height=50)
                layout.remove_widget(instance)
                layout.add_widget(replacement)

            layout = BoxLayout(orientation="vertical")
            for sense in ["Sight","Sound","Touch","Smell","Taste"]:
                btn = Button(text=sense, size_hint_y=None, height=50)
                btn.bind(on_release=lambda btn_instance: replace_widget(btn_instance, sense))
                layout.add_widget(btn)
            
            def on_touch_down(instance, touch):
                if not instance.collide_point(*touch.pos):
                    for child in layout.children:
                        if isinstance(child, TextInput) and not child.text:
                            replace_widget(child, child.hint_text)
                return super(UpdateDistressTol, self).on_touch_down(touch)

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

        elif instance.text == "Pros and Cons":
            self.change(instance, instance.text, instance)

        elif instance.text == "Something else":
            popup_layout = BoxLayout(orientation='vertical')

            # Open a popup with a text input for the user to enter their own skill
            layout = BoxLayout(orientation='vertical')

            def add_more(layout):
                new_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
                layout.add_widget(new_box)

                input = TextInput(hint_text="Tell us here", size_hint_y=None, height=50)
                new_box.add_widget(input)

                more_btn = Button(text="+", size_hint_y=None, width=50, disabled=True)
                more_btn.bind(on_release=add_more(layout))
                new_box.add_widget(more_btn)

                def delete(box):
                    layout.remove_widget(box)
                    if len(layout.children) == 1:
                        add_more(layout)
                del_btn = Button(text="—", size_hint_y=None, width=50, disabled=True)
                del_btn.bind(on_release=delete(new_box))
                new_box.add_widget(del_btn)

                if input.text:
                    more_btn.disabled=False
                    del_btn.disabled=False

                layout.add_widget(new_box)
            
            add_more(layout)
            popup_layout.add_widget(layout)

            submit_btn = Button(text="Submit", size_hint_y=None, width=100)
            def submit(layout):
                for i, child in enumerate(layout.children):
                    for grandchild in child.children:
                        if isinstance(grandchild, TextInput):
                            self.change(grandchild, f"Other {grandchild.text}", instance)
                popup.dismiss()
            submit_btn.bind(on_release=submit(layout))
            popup_layout.add_widget(BoxLayout(size_hint_y=None, height=10))  # Spacer
            popup_layout.add_widget(submit_btn)

            popup = Popup(title="We always love additions to our list.",
                  content=popup_layout,
                  size_hint=(0.8, 0.3))
            popup.open()

    def change(self, instance, skill, original_instance):

        def toggle_color(instance):
            if instance.background_color == [0.39, 0.58, 0.93, 1]:  # Light cornflower blue = was selected before
                instance.background_color = [1, 1, 1, 1]  # Reset to white = unselect
            else:       # was not selected before
                instance.background_color = [0.39, 0.58, 0.93, 1]  # Light cornflower blue = select
        
        if original_instance.text in ["TIPP skills", "Self-soothing"]:     # instance = button, text input
            toggle_color(instance)
            if isinstance(instance, TextInput):
                save_type = f"SelfSoothing_{instance.hint_text}"
                for sense in self.detail_list:
                    if sense in save_type:
                        self.detail_list.replace(sense, skill)
            else:
                save_type = f"{original_instance.text}_{instance.text}"
            if any(x.background_color == [0.39, 0.58, 0.93, 1] for x in instance.parent.children):
                toggle_color(original_instance)
        else:
            toggle_color(original_instance)
            if original_instance.text == "Something else":
                save_type = skill
            else:
                save_type = original_instance.text

        save_type = save_type.replace(" - ", "_")
        self.selected_list.append(save_type.replace(" ", "_"))

    def go_next(self, instance):
        if len(self.selected_dict.items) >= 3:
            db = DBHelper()
            db.create_distress_tolerance_table()
            db.set_preferred_distress_tolerance(self.selected_list, self.detail_list)
            db.close()
            
            done_btn = Button(text="Done", size_hint_y= None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            popup = Popup(title="I'll keep your selections in mind!",
                            content=done_btn,
                            size_hint=(0.8, 0.3))
            self.manager.current = self.manager.previous()
        
        else:
            done_btn = Button(text="Done", size_hint_y= None, width=100)
            done_btn.bind(on_release=popup.dismiss())
            popup = Popup(title="Please select at least three skills.",
                          content=done_btn,
                          size_hint=(0.8, 0.3))
