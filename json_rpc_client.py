import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import json

# Update the start_software function to use the command provided by the user
def start_software():
    """Start the external software process."""
    global process
    command = command_entry.get().strip()
    if not command:
        messagebox.showerror("Error", "Please provide a command to start the software.")
        return

    try:
        process = subprocess.Popen(
            command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start software: {e}")

def send_request():
    """Send JSON request to the external software and display the response."""
    global process
    if not process:
        messagebox.showerror("Error", "Software is not running.")
        return

    try:
        # Get JSON input from the user
        json_input = input_text.get("1.0", tk.END).strip()
        
        # Validate JSON format
        try:
            json.loads(json_input)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")
            return

        # Send JSON input to the software
        process.stdin.write(json_input + "\n")
        process.stdin.flush()

        # Read the response
        response = process.stdout.readline().strip()

        # Display the response in the output area
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, response)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to communicate: {e}")

# Initialize the main application window
root = tk.Tk()
root.title("JSON-RPC Client")

# Add a field for the user to provide the command for starting the external process
command_label = tk.Label(root, text="Command to Start Software:")
command_label.pack(pady=5)

# Add a button next to the command input box to start the process
command_frame = tk.Frame(root)
command_frame.pack(pady=5)

command_entry = tk.Entry(command_frame, width=40)
command_entry.pack(side=tk.LEFT, padx=5)

start_button = tk.Button(command_frame, text="Start Process", command=start_software)
start_button.pack(side=tk.RIGHT)

# Input label and text area
input_label = tk.Label(root, text="JSON Input:")
input_label.pack(pady=5)

input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
input_text.pack(pady=5)

# Send button
send_button = tk.Button(root, text="Send Request", command=send_request)
send_button.pack(pady=5)

# Output label and text area
output_label = tk.Label(root, text="JSON Response:")
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
output_text.pack(pady=5)

# Start the external software when the application starts
process = None

# Run the application
root.mainloop()

# Ensure the process is terminated when the application closes
if process:
    process.terminate()