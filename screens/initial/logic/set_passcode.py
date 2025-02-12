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

class SetPasscodeScreen(Screen):
    def __init__(self, **kwargs):
        super(SetPasscodeScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'set_passcode.kv')
        Builder.load_file(kv_path)
        
        self.passcode = ""
        self.confirm_passcode = ""
        self.is_confirming = False

    def on_key_press(self, instance):
        entered_len = len(self.ids.passcode_input.text)
        if entered_len < 4:
            self.ids.passcode_input.text = "*" * (entered_len-1) + instance.text
            self.passcode += instance.text

        if entered_len == 4:
            if not self.is_confirming:
                self.passcode = self.ids.passcode_input.text
                self.ids.passcode_input.text = ""
                self.ids.label.text = "Confirm code"
                self.is_confirming = True
            else:
                self.confirm_passcode = self.ids.passcode_input.text
                if self.passcode == self.confirm_passcode:
                    userdb = UserHelper()
                    self.new = any(not item for item in userdb.get_user_data())
                    userdb.set_code(self.passcode)
                    userdb.close()
                    self.show_popup("Code Set", "Your passcode has been set successfully.")
                else:
                    self.ids.label.text = "Codes do not match. Try again."
                    self.ids.passcode_input.text = ""
                    self.is_confirming = False

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        next_button = Button(text="Next")
        next_button.bind(on_release=self.go_next)
        content.add_widget(next_button)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def go_next(self, instance):
        if self.new:
            self.manager.current = 'Take_Mindfulness'
        else:
            self.manager.current = 'home'
