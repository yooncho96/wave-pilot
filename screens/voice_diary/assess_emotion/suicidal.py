import tkinter as tk
from tkinter import messagebox
import sys

from kivy.uix.screenmanager import Screen, SlideTransition

class SuicidalScreen(Screen):
    def __init__(self, **kwargs):
        super(SuicidalScreen, self).__init__(**kwargs)

        self.label = tk.Label(self, text="I see you might be in distress right now.", font=("Helvetica", 14), bg='white')
        self.label.pack(pady=20)
        self.after(2000, self.fade_out_label)

    def fade_out_label(self):
        self.label.after(1000, self.label.pack_forget)
        self.after(1000, self.show_question)

    def show_question(self):
        self.label.config(text="Are you having thoughts of killing yourself right now?")
        self.label.pack(pady=20)

        self.yes_button = tk.Button(self, text="Yes", command=self.go_to_crisis)
        self.yes_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.no_button = tk.Button(self, text="No", command=self.no_response)
        self.no_button.pack(side=tk.RIGHT, padx=20, pady=20)

        self.destroy()
        self.no_response()
    
    def go_to_crisis(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'screens/crisis'

    def no_response(self):
        self.label.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        messagebox.showinfo("Response", "Glad to hear it.")
        self.after(2000, self.go_to_record)

    def go_to_record(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'screens/voice_diary/assess_emotion/record'
    
app = SuicidalScreen()
app.mainloop()