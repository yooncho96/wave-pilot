from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from data.user_db_helper import UserHelper
from screens.home import HomeScreen

class TakeCrisisContactScreen(Screen):
    def __init__(self, **kwargs):
        super(TakeCrisisContactScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        title = Label(text="Crisis contacts", font_size=32, size_hint_y=None, height=50)
        self.layout.add_widget(title)
        
        description = Label(
            text="""
            Lastly, we would like to save contact information of two people you trust the most.\n
            We will encourage you to reach out to them when we feel that you are not safe.
            """,
            size_hint_y=None, height=100
        )
        self.layout.add_widget(description)

        for i in range(2):
            self.layout.add_widget(Label(text=f"Your person #{i+1}"))

            box = BoxLayout(orientation="vertical")
            name_input = TextInput(hint_text='Name')
            relationship_input = TextInput(hint_text='Relationship to you')
            phone_input = TextInput(hint_text='Phone')

            box.add_widget(name_input)
            box.add_widget(relationship_input)
            box.add_widget(phone_input)
            self.layout.add_widget(box)

        for child in self.layout.children:
            if isinstance(child, BoxLayout):
                disable = all(field.text for field in child.children)

        self.submit_button = Button(text='Submit', disable=disable)
        self.submit_button.bind(on_press=self.submit)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def submit(self, instance):
        contact_list = []
        for child in self.layout.children:
            if isinstance(child, BoxLayout):
                for field in child.children:
                    contact_list.append(field.text)
        userdb = UserHelper()
        userdb.set_crisis_contact(contact_list)
        userdb.close()

        self.layout.clear_widgets()
        popup_layout = BoxLayout(orientation="vertical")
        popup_layout.add_widget(Label(text="Thank you for all that information.\n Look around and feel free to reach out if you have any questions.\n\n Stay safe,\n WAVE"))
        close_btn = Button(text="Talk to you later")
        close_btn.bind(on_release=self.go_home)
        popup_layout.add_widget(close_btn)
        popup = Popup(title="All done!", content=popup_layout)
        popup.open()

    def go_home(self, instance):
        self.manager.current = HomeScreen