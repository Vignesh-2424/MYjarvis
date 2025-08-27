import os
from modules.nlp_response import get_response
from modules.voice_input import listen_to_user, predict_wake_word

# Auto-launch Spotify app (for Windows)
os.system("start spotify")

print("🤖 Jarvis is ready! Say 'Hey Jarvis' to activate...")

is_active = False

while True:
    if not is_active:
        wake_input = predict_wake_word()
        if wake_input == "postive":
            print("👂 Wake word detected from your voice! I'm listening now.")
            is_active = True
        else:
            print("❌ Say 'Hey Jarvis' to wake me.")
        continue

    # 🔄 Active: normal voice commands
    user_input = listen_to_user()
    if user_input is None:
        continue

    user_input = user_input.lower()

    if user_input in ["exit", "quit", "bye", "go to sleep"]:
        print("👋 Deactivating. Say 'Hey Jarvis' to wake me again.")
        is_active = False
        continue

    reply = get_response(user_input)
    print("🤖 Jarvis:", reply)
