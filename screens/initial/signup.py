# /Users/Apple/Desktop/WAVE-py-v1/screens/initial/signup.py

import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from data.user_db_helper import UserHelper
from screens.initial.set_passcode import SetPasscodeScreen

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.user_id_label = Label(text="Enter your ID:")
        self.add_widget(self.user_id_label)
        self.user_id_entry = TextInput(multiline=False)
        self.add_widget(self.user_id_entry)

        self.email_label = Label(text="Enter your email:")
        self.add_widget(self.email_label)
        self.email_entry = TextInput(multiline=False)
        self.add_widget(self.email_entry)

        self.find_account_button = Button(text="Find Account")
        self.find_account_button.bind(on_press=self.find_account)
        self.add_widget(self.find_account_button)     

    def find_account(self):
        """
        After find account button is clicked,
        check if user_id and email match.
        """
        
        user_id = self.user_id_entry.text
        email = self.email_entry.text

        attempts = 0
        while attempts < 3:
            user_id = self.user_id_entry.text
            email = self.email_entry.text
            userdb = UserHelper()
            userdb.create_user_table()
            found = userdb.find_matching_user(user_id, email)
            userdb.close()

            if found:
                self.password_label = Label(text="Enter your password:")
                self.password_entry = TextInput(password=True, multiline=False)
                self.add_widget(self.password_label)
                self.add_widget(self.password_entry)
                self.submit_button = Button(text="Submit")
                self.submit_button.bind(on_press=self.sign_up)  
                self.add_widget(self.submit_button) 
                break
            else:
                self.show_popup("Error", "User not found.")
                attempts += 1

        if attempts == 3:
            self.show_popup("Error", "Please contact the research team if you cannot remember your ID or registered email.")

    def sign_up(self):
        """
        After submit button is clicked,
        check if password is valid and set it.
        """
        user_id = self.user_id_entry.text
        password = self.password_entry.text
        valid = len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password)

        if valid:
            self.show_popup("Error", "Password must be at least 8 characters long and include both letters and numbers.")
            self.password_entry.text = ''
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
            close_button.bind(on_press=self.landing())
        else:
            close_button.bind(on_press=lambda x: self.close_popup(popup))
        content.add_widget(close_button)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def close_popup(self, popup):
        popup.dismiss()

    def landing(self):
        self.manager.current = SetPasscodeScreen