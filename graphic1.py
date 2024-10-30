import tkinter as tk
from tkinter import scrolledtext
import serial
import time

# Set up serial connection
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# Function to send command
def send_command():
    command = command_entry.get()
    ser.write(command.encode('utf-8') + b'\n')
    time.sleep(0.1)  # Small delay to ensure data is sent
    log_text.insert(tk.END, f"Sent: {command}\n")
    command_entry.delete(0, tk.END)

# Function to read response
def read_response():
    response = ser.readline().decode('utf-8').strip()
    if response:
        log_text.insert(tk.END, f"Received: {response}\n")
    log_text.see(tk.END)  # Scroll to the end

# Set up the GUI window
root = tk.Tk()
root.title("UART Communication")

# Command entry
command_entry = tk.Entry(root, width=50)
command_entry.pack(pady=5)

# Send button
send_button = tk.Button(root, text="Send", command=send_command)
send_button.pack(pady=5)

# Response log
log_text = scrolledtext.ScrolledText(root, width=60, height=20, state='normal')
log_text.pack(pady=5)

# Read button to manually get a response
read_button = tk.Button(root, text="Read Response", command=read_response)
read_button.pack(pady=5)

# Main loop
root.mainloop()

# Close the serial connection on exit
ser.close()
