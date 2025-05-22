from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class Gui:
    def __init__(self):
        self.process = None

    def setup(self):

        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Command input
        command_label = Label(text="Command to Start Software:")
        self.layout.add_widget(command_label)

        command_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.command_input = TextInput(hint_text="Enter command", multiline=False)
        command_box.add_widget(self.command_input)
        start_button = Button(text="Start Process", size_hint_x=None, width=120)
        command_box.add_widget(start_button)
        self.layout.add_widget(command_box)

        # Input area
        input_label = Label(text="Input:")
        self.layout.add_widget(input_label)

        self.input_text = TextInput(hint_text="Enter JSON input", multiline=True, size_hint_y=None, height=150)
        self.layout.add_widget(self.input_text)

        send_button = Button(text="Send Request", size_hint_y=None, height=40)
        self.layout.add_widget(send_button)

        # Output area
        output_label = Label(text="STDOUT:")
        self.layout.add_widget(output_label)

        self.output_text = TextInput(readonly=True, size_hint_y=None, height=150)
        self.layout.add_widget(self.output_text)

        stderr_label = Label(text="STDERR:")
        self.layout.add_widget(stderr_label)

        self.stderr_text = TextInput(readonly=True, size_hint_y=None, height=150)
        self.layout.add_widget(self.stderr_text)

        return self.layout

    def run(self):
        print("GUI is running")