from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

class BorderedLabel(Label):
    """ Custom Label with a border """
    def __init__(self, thick_border=False, **kwargs):
        super().__init__(**kwargs)
        self.thick_border = thick_border
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black border
            border_width = 3 if self.thick_border else 1
            Rectangle(pos=(self.x - border_width / 2, self.y - border_width / 2),
                      size=(self.width + border_width, self.height + border_width))

class BorderedTextInput(TextInput):
    """ Custom TextInput with a border """
    def __init__(self, key, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.parent_screen = parent_screen
        self.multiline = False
        self.bind(text=self.update_value)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_value(self, instance, value):
        """ Update the dictionary with the entered value """
        self.parent_screen.input_values[self.key] = value

    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black border
            Rectangle(pos=self.pos, size=self.size)