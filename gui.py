import tkinter as tk
from tkinter import messagebox
from modules.voice_input import listen_to_user
from modules.nlp_response import get_response

# Global state for wake word
is_active = False

def start_jarvis():
    global is_active

    user_input = listen_to_user()
    
    if user_input is None:
        response_entry.set("I didn't hear you.")
        return

    user_input = user_input.lower()
    user_entry.set(user_input)

    # Check if Jarvis is not yet active (waiting for wake word)
    if not is_active:
        if user_input.startswith("hey jarvis"):
            is_active = True
            response_entry.set("👂 Wake word detected! I'm listening now.")
        else:
            response_entry.set("❌ Say 'Hey Jarvis' to wake me.")
        return

    # Deactivation commands
    if user_input in ["exit", "quit", "bye", "go to sleep"]:
        is_active = False
        response_entry.set("👋 Deactivating. Say 'Hey Jarvis' to wake me again.")
        return

    # Get normal response from NLP
    response = get_response(user_input)
    response_entry.set("🤖 " + response)

# Create the main window
root = tk.Tk()
root.title("Jarvis Assistant 🤖")
root.geometry("500x300")
root.configure(bg="#1e1e1e")

# Input and Output variables
user_entry = tk.StringVar()
response_entry = tk.StringVar()

# GUI Layout
tk.Label(root, text="🗣️ You said:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
tk.Entry(root, textvariable=user_entry, width=60, font=("Arial", 12)).pack(pady=5)

tk.Label(root, text="🤖 Jarvis says:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(20, 0))
tk.Entry(root, textvariable=response_entry, width=60, font=("Arial", 12)).pack(pady=5)

tk.Button(root, text="🎙 Start Listening", font=("Arial", 14), command=start_jarvis, bg="#007acc", fg="white").pack(pady=20)

# Run the app
root.mainloop()
