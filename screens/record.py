# screens/speech.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from data.emotion_db_helper import DBHelper
from openai_api.openai_helper import transcribe_audio_via_openai, get_emotion_scores


class SpeechScreen(Screen):
    """
    Screen to handle local audio file input, transcribe it,
    and get emotion scores from OpenAI.
    """
    def __init__(self, **kwargs):
        super(SpeechScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        instr_label = Label(text="Enter the path to your audio file:", font_size=18)
        layout.add_widget(instr_label)

        self.audio_path_input = TextInput(hint_text="e.g., /path/to/file.wav", size_hint=(1, 0.1))
        layout.add_widget(self.audio_path_input)

        self.transcription_label = Label(text="Transcription will appear here", font_size=14)
        layout.add_widget(self.transcription_label)

        transcribe_btn = Button(text="Transcribe & Analyze Emotions", size_hint=(1, 0.1))
        transcribe_btn.bind(on_release=self.on_transcribe)
        layout.add_widget(transcribe_btn)

        back_btn = Button(text="Back to Home", size_hint=(1, 0.1))
        back_btn.bind(on_release=self.go_back_home)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_transcribe(self, instance):
        audio_path = self.audio_path_input.text.strip()
        if not audio_path:
            self.transcription_label.text = "Please provide an audio file path."
            return

        # 1) Transcribe
        transcript = transcribe_audio_via_openai(audio_path)
        if not transcript:
            self.transcription_label.text = "Transcription failed or returned empty."
            return

        self.transcription_label.text = f"Transcript:\n{transcript}"

        # 2) Get emotion scores
        scores = get_emotion_scores(transcript)

        # 3) Store in DB
        db = DBHelper()
        db.create_emotion_table()
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

        self.transcription_label.text += "\n\nEmotion scores saved to DB."

    def go_back_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home_screen"
