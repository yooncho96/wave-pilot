from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder

import os
import sounddevice as sd
import numpy as np
import wave

from data.diary_db_Helper import DBHelper
from openai_api.openai_helper import transcribe_audio_via_openai, get_emotion_scores

class RecordScreen(Screen):
    """
    Screen to handle local audio file input, transcribe it,
    and get emotion scores from OpenAI.
    """
    def __init__(self, **kwargs):
        super(RecordScreen, self).__init__(**kwargs)
        kv_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'record.kv')
        Builder.load_file(kv_path)

    def start_recording(self, instance):
        self.fs = 44100  # Sample rate
        self.duration = float('inf')  # Duration of recording in seconds (infinite)
        self.recording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2, dtype='int16')
        sd.wait()

    def pause_recording(self, instance):
        sd.stop()
        if not hasattr(self, 'recording_data'):
            self.recording_data = self.recording.copy()
        else:
            self.recording_data = np.append(self.recording_data, self.recording, axis=0)

    def on_transcribe(self, instance):
        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(self.recording_data.tobytes())
        audio_path = "temp.wav"

        popup = Popup(title="Processing", content=Label(text="Feeling all the feelings"), size_hint=(0.6, 0.2))
        popup.open()

        def update_popup_text(dt):
            if popup.content.text.endswith("..."):
                popup.content.text = "Feeling all the feelings"
            else:
                popup.content.text += "."

        self.popup_event = Clock.schedule_interval(update_popup_text, 0.5)

        transcript = transcribe_audio_via_openai(audio_path)

        db = DBHelper()
        db.create_emotion_table()

        scores = get_emotion_scores(transcript)

        db.insert_emotion_data(
            transcript,
            scores.get("anger", 0),
            scores.get("sadness", 0),
            scores.get("fear", 0),
            scores.get("shame", 0),
            scores.get("guilt", 0),
            scores.get("jealousy", 0),
            scores.get("envy", 0),
            scores.get("joy", 0),
            scores.get("love", 0)
        )
        db.close()

        popup.dismiss()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'confirm_emotion'

    def go_back_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
