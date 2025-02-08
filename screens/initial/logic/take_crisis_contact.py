from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

from data.user_db_helper import UserHelper

class TakeCrisisContactScreen(Screen):
    def __init__(self, **kwargs):
        super(TakeCrisisContactScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'take_crisis_contact.kv')
        Builder.load_file(kv_path)

    def submit(self, instance):
        contact_list = []
        for i in range(1, 3):
            name = self.ids[f'name_input_{i}'].text
            relationship = self.ids[f'relationship_input_{i}'].text
            phone = self.ids[f'phone_input_{i}'].text
            contact_list.append({'name': name, 'relationship': relationship, 'phone': phone})

        userdb = UserHelper()
        userdb.set_crisis_contact(contact_list)
        userdb.close()

        self.show_popup("All done!", "Thank you for all that information.\nLook around and feel free to reach out if you have any questions.\n\nStay safe,\nWAVE")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text=message))
        close_btn = Button(text="Talk to you later")
        close_btn.bind(on_release=self.go_home)
        popup_layout.add_widget(close_btn)
        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(400, 400))
        popup.open()

    def go_home(self, instance):
        self.manager.current = 'home'
