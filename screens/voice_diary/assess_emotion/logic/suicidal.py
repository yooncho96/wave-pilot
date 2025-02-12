from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.clock import Clock
import os


class SuicidalScreen(Screen):
    def __init__(self, **kwargs):
        super(SuicidalScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'suicidal.kv')
        Builder.load_file(kv_path)

        Clock.schedule_once(self.fade_out_label, 2)

    def fade_out_label(self, dt):
        self.ids.intro_label.opacity = 0
        Clock.schedule_once(self.show_question, dt)

    def show_question(self, dt):
        self.ids.intro_label.text = "Are you having thoughts of killing yourself right now?"
        self.ids.intro_label.opacity = 1
        self.ids.button_layout.opacity = 1

    def go_to_crisis(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'crisis'

    def no_response(self, instance):
        self.ids.intro_label.text = "Glad to hear it."
        self.ids.button_layout.opacity = 0
        Clock.schedule_once(self.go_to_record, 2)

    def go_to_record(self, dt):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'record'
