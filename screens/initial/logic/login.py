from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

from data.user_db_helper import UserHelper

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'login.kv')
        Builder.load_file(kv_path)
        self.passcode = ""

    def add_digit(self, instance):
        if len(self.passcode) < 4:
            self.passcode += instance.text
            self.ids.passcode_input.text = '*' * len(self.passcode)
        if len(self.passcode) == 4:
            self.check_passcode()

    def check_passcode(self):
        userdb = UserHelper()
        correct = userdb.login(self.passcode)
        userdb.close()
        if correct:
            self.manager.current = 'home'
        else:
            self.ids.label.text = "Code does not match"
            self.ids.forgot_button.opacity = 1
            self.passcode = ""
            self.ids.passcode_input.text = ""

    def forgot_passcode(self, instance):
        self.ids.layout.clear_widgets()
        self.ids.label.text = "Let's try your password."

        self.password_input = TextInput(hint_text="Password", font_size=32, halign='center')
        self.ids.layout.add_widget(self.password_input)

        box = BoxLayout(orientation='horizontal')
        submit_button = Button(text="Submit", size_hint_x=None, width=200)
        submit_button.bind(on_press=self.check_password)
        forgot_button = Button(text="Forgot password?", size_hint_x=None, width=200)
        forgot_button.bind(on_press=self.forgot_password)
        box.add_widget(submit_button)
        box.add_widget(forgot_button)
        self.ids.layout.add_widget(box)

    def check_password(self, instance):
        userdb = UserHelper()
        true_password = userdb.get_password()
        userdb.close()
        if self.password_input.text == true_password:
            self.manager.current = 'home'
        else:
            self.ids.label.text = "Password does not match"
            self.password_input.text = ""
    
    def forgot_password(self, instance):
        content = BoxLayout(orientation='vertical')
        message = Label(text="You will need to enter your ID and registered email again. If you don't remember them, please contact the research team.")
        ok_button = Button(text="OK", size_hint_y=None, height=50)
        content.add_widget(message)
        content.add_widget(ok_button)

        popup = Popup(title='Forgot Password', content=content, size_hint=(0.8, 0.5))
        ok_button.bind(on_press=lambda x: self.goto_signup(popup))
        popup.open()

    def goto_signup(self, popup):
        popup.dismiss()
        self.manager.current = 'signup'
