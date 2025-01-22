# screens/emotion_data.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from data.emotion_db_helper import DBHelper

class EmotionDataScreen(Screen):
    """
    Screen to display all stored emotion data (ID, transcript, and emotion scores).
    """
    def __init__(self, **kwargs):
        super(EmotionDataScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.data_label = Label(text="No data loaded yet.", font_size=14)
        self.layout.add_widget(self.data_label)

        refresh_btn = Button(text="Refresh Data", size_hint=(1, 0.1))
        refresh_btn.bind(on_release=self.load_data)
        self.layout.add_widget(refresh_btn)

        back_btn = Button(text="Back to Home", size_hint=(1, 0.1))
        back_btn.bind(on_release=self.go_back_home)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def load_data(self, instance):
        db = DBHelper()
        db.create_emotion_table()
        rows = db.get_all_emotion_data()
        db.close()

        lines = []
        for row in rows:
            row_id, transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love = row
            line = (
                f"ID: {row_id}\n"
                f"Transcript: {transcript}\n"
                f"anger={anger}, sadness={sadness}, fear={fear}, shame={shame}, guilt={guilt}\n"
                f"jealousy={jealousy}, envy={envy}, joy={joy}, love={love}"
            )
            lines.append(line + "\n" + "-"*50)

        if lines:
            self.data_label.text = "\n\n".join(lines)
        else:
            self.data_label.text = "No data found."

    def go_back_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home_screen"
