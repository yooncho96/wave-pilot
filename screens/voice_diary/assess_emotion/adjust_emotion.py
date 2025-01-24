from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider

import json

from data.db_helper import DBHelper

class AdjustEmotionScreen(Screen):
    """
    1) Apologize
    2) Present all top 3 emotions, each with a sliding scale (0-10) displaying analysis results, \n
        and ask to adjust accordingly\n
        Include another option "Other"
    3) If "other" chosen, show multiple choice of all emotion names\n
        When chosen, show sliding scale (0-10) 
    """
    def __init__(self, **kwargs):
        super(AdjustEmotionScreen, self).__init__(**kwargs)
        self.db_helper = DBHelper()
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.create_ui()

    def create_ui(self):
        self.layout.clear_widgets()
        
        # Apologize
        self.layout.add_widget(Label(
            text="""
                I apologize. Can you help me get to know you better?\n
            """
        ))
        self.layout.add_widget(Label(
            text="Please choose the emotion that is closest to what you feel.\n You can correct the rating if you wish.",
            italic=True,
            font_size='12sp'
        ))

    def create_slider(self, value):
        slider_layout = BoxLayout(orientation='horizontal')
        slider = Slider(min=0, max=10, value=value)
        slider_layout.add_widget(slider)
        return slider_layout

    def show_other_emotions(self, instance):

        # Present all emotions in sorted order
        db = DBHelper()
        first_try = db.get_emotion_data()
        db.close()

        sorted_emotions = [x for x in first_try.keys()]

        left_layout = BoxLayout(orientation='vertical')
        right_layout = BoxLayout(orientation='vertical')

        for i, emotion in enumerate(sorted_emotions):
            if i==0:
                label = Label(text=f"1st:", size_hint_x=0.1)
            elif i==1:
                label = Label(text=f"2nd:", size_hint_x=0.1)
            elif i==2:
                label = Label(text=f"3rd:", size_hint_x=0.1)
            else:
                label = Label(text=f"{i+1}th:", size_hint_x=0.1)
            
            button = Button(text=emotion, size_hint_x=0.9)
            button.bind(on_release=self.select_emotion)
            emotion_layout = BoxLayout(orientation='horizontal')
            emotion_layout.add_widget(label)
            emotion_layout.add_widget(button)

            if i < 5:
                left_layout.add_widget(emotion_layout)
            else:
                right_layout.add_widget(emotion_layout)
        
        self.layout.add_widget(left_layout)
        self.layout.add_widget(right_layout)

    def select_emotion(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(
            text="How strong is this emotion right now?",
            font_size='16sp'
        ))
        self.layout.add_widget(Label(
            text=instance.text,
            font_size='14sp',
            bold=True
        ))
        self.layout.add_widget(self.create_slider(0))
        next_button = Button(text="Next", size_hint=(1, 0.1))
        next_button.bind(on_release=self.submit_emotion)
        self.layout.add_widget(next_button)
        
    def submit_emotion(self, instance):
        # retrieve the number (float, 1 decimal) from the slider
        slider_value = self.layout.children[1].children[0].value
        emotion = self.layout.children[2].text
        # Save the emotion and its value to the database
        self.db_helper.adjust_emotion({emotion: round(slider_value, 1)})

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'screens/voice_diary/skill_willingness'

        