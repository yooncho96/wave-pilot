# screens/speech.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from data.db_helper import DBHelper
from openai_api.openai_helper import transcribe_audio_via_openai, get_emotion_scores
import sounddevice as sd
import numpy as np
import wave


class SpeechScreen(Screen):
    """
    Screen to handle local audio file input, transcribe it,
    and get emotion scores from OpenAI.
    """
    def __init__(self, **kwargs):
        super(SpeechScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        record_btn = Button(text="Record", size_hint=(1, 0.1))
        record_btn.bind(on_press=self.start_recording)
        record_btn.bind(on_release=self.pause_recording)
        layout.add_widget(record_btn)

        transcribe_btn = Button(text="Transcribe", size_hint=(1, 0.1))
        transcribe_btn.bind(on_release=self.on_transcribe)
        layout.add_widget(transcribe_btn)

        back_btn = Button(text="Back to Home", size_hint=(1, 0.1))
        back_btn.bind(on_release=self.go_back_home)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def start_recording(self, instance):
        self.fs = 44100  # Sample rate
        self.duration = float('inf')  # Duration of recording in seconds (infinite)
        self.recording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2, dtype='int16')
        sd.wait()

    def pause_recording(self, instance):
        sd.stop()
        # if triggered first time
        if not hasattr(self, 'recording_data'):
            self.recording_data = self.recording.copy()
        # if triggered more than once, append new recording to existing recording_data
        else:
            self.recording_data = np.append(self.recording_data, self.recording, axis=0)   

    def on_transcribe(self, instance):

        # temporarily save the recording to a .wav file
        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(self.recording_data.tobytes())
        audio_path = "temp.wav"

        # 1) Transcribe

        # Show pop-up
        popup = Label(text="Feeling all the feelings")
        popup.size_hint = (0.6, 0.2)
        popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(popup)

        def update_popup_text(dt):
            if popup.text.endswith("..."):
                popup.text = "Feeling all the feelings"
            else:
                popup.text += "."

        self.popup_event = Clock.schedule_interval(update_popup_text, 0.5)

        transcript = transcribe_audio_via_openai(audio_path)

        # if not transcript:
        #     self.transcription_label.text = "Transcription failed or returned empty."
        #     return

        db = DBHelper()
        db.create_emotion_table()

        # 2) Get emotion scores
        scores = get_emotion_scores(transcript)

        # 3) Store in DB
        db.insert_emotion_data(
            transcript,
            scores["anger"],
            scores["sadness"],
            scores["fear"],
            scores["shame"],
            scores["guilt"],
            scores["jealousy"],
            scores["envy"],
            scores["joy"],
            scores["love"]
        )
        db.close()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'confirm_emotion'

    def go_back_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home_screen"
