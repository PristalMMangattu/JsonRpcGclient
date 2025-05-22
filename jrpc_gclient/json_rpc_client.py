from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import subprocess
import json
from gui import Gui

class JsonRpcClientApp(App):
    def build(self):
        self.gui = Gui()
        layout = self.gui.setup()

        # Bind buttons to methods
        start_button = self.gui.layout.children[1].children[1]  # Corrected index for Start Process button
        send_button = self.gui.layout.children[0]  # Corrected index for Send Request button

        start_button.bind(on_press=self.start_software)
        send_button.bind(on_press=self.send_request)

        return layout

    def start_software(self, instance):
        command = self.gui.command_input.text.strip()
        if not command:
            self.show_error("Error", "Please provide a command to start the software.")
            return

        try:
            self.gui.process = subprocess.Popen(
                command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            self.show_error("Error", f"Failed to start software: {e}")

    def send_request(self, instance):
        if not self.gui.process:
            self.show_error("Error", "Software is not running.")
            return

        json_input = self.gui.input_text.text.strip()
        try:
            json.loads(json_input)  # Validate JSON format
        except json.JSONDecodeError:
            self.show_error("Error", "Invalid JSON format.")
            return

        try:
            self.gui.process.stdin.write(json_input + "\n")
            self.gui.process.stdin.flush()

            response = self.gui.process.stdout.readline().strip()
            self.gui.output_text.text = response

            stderr_output = self.gui.process.stderr.readline().strip()
            self.gui.stderr_text.text = stderr_output
        except Exception as e:
            self.show_error("Error", f"Failed to communicate: {e}")

    def show_error(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def on_stop(self):
        if self.gui.process:
            self.gui.process.terminate()

if __name__ == "__main__":
    JsonRpcClientApp().run()