from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

from data.user_db_helper import UserHelper

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'signup.kv')
        Builder.load_file(kv_path)

    def find_account(self):
        user_id = self.ids.user_id_entry.text
        email = self.ids.email_entry.text

        userdb = UserHelper()
        userdb.create_user_table()
        found = userdb.find_matching_user(user_id, email)
        userdb.close()

        if found:
            self.ids.password_label.opacity = 1
            self.ids.password_entry.opacity = 1
            self.ids.submit_button.opacity = 1
        else:
            self.show_popup("Error", "User not found.")

    def sign_up(self):
        user_id = self.ids.user_id_entry.text
        password = self.ids.password_entry.text

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            self.show_popup("Error", "Password must be at least 8 characters long and include both letters and numbers.")
            self.ids.password_entry.text = ''
        else:
            userdb = UserHelper()
            userdb.set_pw(user_id, password)
            userdb.close()
            self.show_popup("Success", "Password set.")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Close")
        if title == "Success":
            close_button.bind(on_release=self.landing)
        else:
            close_button.bind(on_release=lambda x: popup.dismiss())
        content.add_widget(close_button)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def landing(self, instance):
        self.manager.current = 'set_passcode'
