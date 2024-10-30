import tkinter as tk
from tkinter import scrolledtext
import serial
import time
import threading

# Set up serial connection
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# Function to send command from a specific text entry box
def send_command(entry):
    command = entry.get()
    ser.write(command.encode('utf-8') + b'\n')
    time.sleep(0.1)  # Small delay to ensure data is sent
    log_text.insert(tk.END, f"Sent: {command}\n")
    log_text.see(tk.END)

# Function to continuously read responses and update log
def read_response():
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            if response:
                log_text.insert(tk.END, f"Received: {response}\n")
                log_text.see(tk.END)
        time.sleep(0.1)  # Small delay to avoid high CPU usage

# Set up the GUI window
root = tk.Tk()
root.title("UART Communication")

# Create 5 text entry boxes with a send button beside each
entries = []

# Manually specify the commands for each entry box
commands = [
    "command1",  # Change this to your desired command
    "command2",  # Change this to your desired command
    "command3",  # Change this to your desired command
    "command4",  # Change this to your desired command
    "command5"   # Change this to your desired command
]

for command in commands:
    frame = tk.Frame(root)
    frame.pack(pady=2)

    entry = tk.Entry(frame, width=40)
    entry.insert(0, command)  # Prefill with specified command
    entry.pack(side=tk.LEFT, padx=5)
    entries.append(entry)

    send_button = tk.Button(frame, text="Send", command=lambda e=entry: send_command(e))
    send_button.pack(side=tk.RIGHT, padx=5)

# Response log
log_text = scrolledtext.ScrolledText(root, width=60, height=20, state='normal')
log_text.pack(pady=5)

# Start a thread to continuously read responses
response_thread = threading.Thread(target=read_response, daemon=True)
response_thread.start()

# Main loop
root.mainloop()

# Close the serial connection on exit
ser.close()
