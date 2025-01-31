from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.core.window import Window
from math import radians


class CircularProgressBar(Widget):
    """ Custom Circular Progress Bar (Decreasing Clockwise) """
    def __init__(self, max_progress, **kwargs):
        super().__init__(**kwargs)
        self.max_progress = max_progress
        self.progress = max_progress
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def set_progress(self, value):
        """ Update progress and redraw """
        self.progress = max(0, min(self.max_progress, value))
        self.update_canvas()

    def update_canvas(self, *args):
        """ Draw circular progress bar decreasing clockwise """
        self.canvas.clear()
        with self.canvas:
            # Background Circle
            Color(0.7, 0.85, 1, 1)  # Soft light blue background
            Ellipse(pos=self.pos, size=self.size)

            # Progress Arc (Clockwise)
            if self.progress > 0:
                Color(0, 0, 0.8, 1)  # Dark blue progress
                start_angle = 360 * (self.progress / self.max_progress)
                Line(circle=(self.center_x, self.center_y, self.width / 2, 0, start_angle), width=8)

class Timer(BoxLayout):
    def __init__(self, time_in_minutes=1, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)
        self.original_time = time_in_minutes * 60
        self.time_in_seconds = self.original_time
        self.running = False

        # Circular Progress Bar (Big and Centered)
        self.progress_bar = CircularProgressBar(max_progress=self.original_time, size_hint=(None, None), size=(250, 250))

        # Button Layout (Small Buttons Below)
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.start_button = Button(text="Play", font_size="20sp", size_hint=(None, None), size=(120, 60), on_press=self.toggle_timer)
        self.reset_button = Button(text="Reset", font_size="20sp", size_hint=(None, None), size=(120, 60), on_press=self.reset_timer)

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.reset_button)

        # Center Align Widgets
        self.progress_bar.pos_hint = {"center_x": 0.5}
        self.start_button.pos_hint = {"center_x": 0.5}
        self.reset_button.pos_hint = {"center_x": 0.5}

        # Center Align Layout
        self.add_widget(self.progress_bar)  # Large Circular Timer
        self.add_widget(button_layout)  # Small Buttons Below

    def toggle_timer(self, instance):
        """ Start or Pause the timer """
        if self.running:
            self.running = False
            self.start_button.text = "Start"
            Clock.unschedule(self.update_time)
        else:
            self.running = True
            self.start_button.text = "Pause"
            Clock.schedule_interval(self.update_time, 1)

    def reset_timer(self, instance):
        """ Reset timer to original time_in_minutes """
        self.running = False
        self.start_button.text = "Start"
        Clock.unschedule(self.update_time)
        self.time_in_seconds = self.original_time  # Reset to original time
        self.progress_bar.set_progress(self.original_time)  # Reset circular progress bar

    def update_time(self, dt):
        """ Update circular progress bar countdown """
        if self.time_in_seconds > 0:
            self.time_in_seconds -= 1
            self.progress_bar.set_progress(self.time_in_seconds)
        else:
            self.running = False
            self.start_button.text = "▶"
            Clock.unschedule(self.update_time)

