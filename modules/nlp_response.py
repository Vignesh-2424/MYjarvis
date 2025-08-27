import subprocess
import pyttsx3
import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser

from modules.memory import (
    load_memory,
    update_memory,
    add_reminder,
    get_reminders_for_date,
    save_memory,
)

from modules.spotify_control import play_song, pause_music, resume_music, stop_music  # ✅ Spotify control

engine = pyttsx3.init()

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def get_response(prompt: str):
    if not prompt:
        return "I didn't catch that, sir."

    prompt = prompt.strip()
    prompt_lower = prompt.lower()

    # ✅ Spotify voice command handling
    if prompt_lower.startswith("play ") and "on spotify" in prompt_lower:
        song_name = prompt_lower.replace("play", "").replace("on spotify", "").strip()
        play_song(song_name)
        return f"Playing {song_name} on Spotify."

    if "pause music" in prompt_lower or "pause song" in prompt_lower:
        pause_music()
        return "Paused music on Spotify."

    if "resume music" in prompt_lower or "continue music" in prompt_lower:
        resume_music()
        return "Resumed music on Spotify."

    if "stop music" in prompt_lower or "stop song" in prompt_lower:
        stop_music()
        return "Stopped music on Spotify."

    memory = load_memory()
    personal = memory.get("personal", {})
    history = memory.get("history", [])
    user_name = personal.get("name", "sir")
    memory_context = "\n".join([f"{k}: {v}" for k, v in personal.items()])

    # Date
    if "what's the date" in prompt_lower or "what is today's date" in prompt_lower:
        today = datetime.now().strftime("%A, %d %B %Y")
        response = f"Today is {today}"
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response

    # Time
    if "what time is it" in prompt_lower or "current time" in prompt_lower:
        current_time = datetime.now().strftime("%I:%M %p")
        response = f"It's {current_time} right now"
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response

    # Today's tasks
    if "what is pending today" in prompt_lower:
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_tasks = get_reminders_for_date(today_str)
        response = "Here’s what’s pending today:\n" + "\n".join(f"- {t}" for t in today_tasks) if today_tasks else "No pending tasks today, sir."
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response

    # This week's tasks
    if "what's coming this week" in prompt_lower or "this week's tasks" in prompt_lower:
        today = datetime.now().date()
        upcoming = []
        for i in range(7):
            day = today + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            tasks = memory.get("reminders", {}).get(day_str, [])
            for task in tasks:
                upcoming.append(f"{day_str}: {task}")
        response = "Here's what’s coming up this week:\n" + "\n".join(upcoming) if upcoming else "No tasks scheduled for this week."
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response

    # Add reminder (natural language date)
    if "remind me" in prompt_lower:
        match = re.search(r"remind me to (.+?) on (.+)", prompt_lower)
        if match:
            task = match.group(1).strip()
            spoken_date = match.group(2).strip()
            try:
                parsed_date = date_parser.parse(spoken_date, fuzzy=True)
                date_str = parsed_date.strftime("%Y-%m-%d")
                add_reminder(date_str, task)
                memory = load_memory()
                response = f"Reminder added for {date_str}: {task}"
            except ValueError:
                response = "I couldn't understand the date. Please say it clearly like '25th June 2025' or 'March 1 2025'."
        else:
            response = "Please say something like 'remind me to take tablets on 25th June 2025'."
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response

    # Delete reminder
    if "delete reminder" in prompt_lower or "remove reminder" in prompt_lower:
        match = re.search(r"(?:delete|remove) reminder (.+)", prompt_lower)
        if match:
            task_to_remove = match.group(1).strip().lower()
            removed = False
            reminders = memory.get("reminders", {})
            for date_str, tasks in list(reminders.items()):
                new_tasks = [t for t in tasks if task_to_remove not in t.lower()]
                if len(new_tasks) != len(tasks):
                    memory["reminders"][date_str] = new_tasks
                    removed = True
            response = "Reminder removed." if removed else "I couldn't find that reminder."
            memory["history"] = history + [{"user": prompt, "jarvis": response}]
            save_memory(memory)
            speak(response)
            return response

    # Learn name
    if "my name is" in prompt_lower:
        name = prompt.split("my name is")[-1].strip().split()[0]
        update_memory("name", name, section="personal")
        response = f"Nice to meet you, {name}!"
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response

    # Remember fact
    if "remember" in prompt_lower:
        parts = prompt.split("remember")
        if len(parts) > 1:
            fact = parts[-1].strip()
            update_memory(fact, "saved", section="personal")
            response = "Got it! I'll remember that."
            history.append({"user": prompt, "jarvis": response})
            memory["history"] = history
            save_memory(memory)
            speak(response)
            return response

    # Fallback to Ollama
    recent_history = history[-5:]
    history_context = "\n".join(f"User: {h['user']}\nJarvis: {h['jarvis']}" for h in recent_history)

    context = f"""
You are Jarvis, a smart, casual, and kind AI assistant.
You are the best friend of {user_name}.
Use the following facts to sound more personal:
{memory_context}

Recent conversation history:
{history_context}

The user said: {prompt}
Reply naturally, casually, and like you're talking to a close friend.
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "nous-hermes2"],
            input=context.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        response = result.stdout.decode().strip()
        history.append({"user": prompt, "jarvis": response})
        memory["history"] = history
        save_memory(memory)
        speak(response)
        return response
    except Exception as e:
        return f"Error getting response: {e}"
