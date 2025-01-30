from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from data.user_db_helper import UserHelper
from screens.initial.take_mindfulness_skill import MindfulnessScreen

class SetPasscodeScreen(Screen):
    def __init__(self, **kwargs):
        super(SetPasscodeScreen, self).__init__(**kwargs)
        self.passcode = ""
        self.confirm_passcode = ""
        self.is_confirming = False

        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Enter your 4-digit code.\n You will enter this code every time you access WAVE.", font_size=24)
        self.layout.add_widget(self.label)

        self.passcode_input = TextInput(password=True, readonly=True, font_size=24, halign='center')
        self.layout.add_widget(self.passcode_input)

        self.keypad = GridLayout(cols=3)
        for i in range(1, 10):
            self.keypad.add_widget(Button(text=str(i), on_press=self.on_key_press))
        self.keypad.add_widget(Button(text='0', on_press=self.on_key_press))
        self.layout.add_widget(self.keypad)

        self.add_widget(self.layout)

    def on_key_press(self, instance):
        if len(self.passcode_input.text) < 4:
            self.passcode_input.text += instance.text

        if len(self.passcode_input.text) == 4:
            if not self.is_confirming:
                self.passcode = self.passcode_input.text
                self.passcode_input.text = ""
                self.label.text = "Confirm code"
                self.is_confirming = True
            else:
                self.confirm_passcode = self.passcode_input.text
                if self.passcode == self.confirm_passcode:
                    userdb = UserHelper()
                    userdb.set_code(self.passcode)
                    userdb.close()
                    self.next_button = Button(text="Next", on_press=self.go_next)
                    self.popup = Popup(title='Code Set', content=self.next_button, size_hint=(None, None), size=(400, 400))
                else:
                    self.label.text = "Codes do not match. Try again."
                    self.passcode_input.text = ""
                    self.is_confirming = False

    def go_next(self):
        self.manager.current = MindfulnessScreen