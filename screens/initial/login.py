from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from data.user_db_helper import UserHelper
from kivy.uix.popup import Popup

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.passcode = ""

        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="CODE", font_size=32)
        self.layout.add_widget(self.label)

        self.passcode_input = TextInput(password=True, readonly=True, font_size=32, halign='center')
        self.layout.add_widget(self.passcode_input)

        self.keypad = GridLayout(cols=3)
        for i in range(1, 10):
            self.keypad.add_widget(Button(text=str(i), on_press=self.add_digit))
        self.keypad.add_widget(Button(text='0', on_press=self.add_digit))
        self.layout.add_widget(self.keypad)

        self.forgot_button = Button(text="Forgot code?", size_hint_y=None, height=50)
        self.forgot_button.bind(on_press=self.forgot_passcode)
        self.forgot_button.opacity = 0
        self.layout.add_widget(self.forgot_button)

        self.add_widget(self.layout)

    def add_digit(self, instance):
        if len(self.passcode) < 4:
            self.passcode += instance.text
            self.passcode_input.text = '*' * len(self.passcode)
        if len(self.passcode) == 4:
            self.check_passcode()

    def check_passcode(self):
        userdb = UserHelper()
        correct = userdb.login(self.passcode)
        userdb.close()
        if correct:
            self.manager.current = 'screens/home'
        else:
            self.label.text = "Code does not match"
            self.forgot_button.opacity = 1
            self.passcode = ""
            self.passcode_input.text = ""

    def forgot_passcode(self, instance):
        self.layout.clear_widgets()
        self.label = Label(text="Let's try your password.", font_size=32)
        self.layout.add_widget(self.label)

        self.password_input = TextInput(hint_text="Password", font_size=32, halign='center')
        self.layout.add_widget(self.password_input)

        self.box = BoxLayout(orientation='horizontal')
        self.submit_button = Button(text="Submit", size_hint_x=None, width=200)
        self.submit_button.bind(on_press=self.check_password())
        self.forgot_button2 = Button(text="Forgot password?", size_hint_x=None, width=200)
        self.forgot_button2.bind(on_press=self.forgot_password())
        self.box.add_widget(self.submit_button)
        self.box.add_widget(self.forgot_button2)
        self.layout.add_widget(self.box)

    def check_password(self, instance):
        userdb = UserHelper()
        true_password = userdb.get_password()
        userdb.close()
        if self.password_input.text == true_password:
            self.manager.current = 'screens/home'
        else:
            self.label.text = "Password does not match"
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
        self.manager.current = 'screens/initial/signup'