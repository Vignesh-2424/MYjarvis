import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(key, value, section="personal"):
    memory = load_memory()
    if section not in memory or not isinstance(memory[section], dict):
        memory[section] = {}
    memory[section][key] = value
    save_memory(memory)

def add_reminder(date, task):
    memory = load_memory()
    if "reminders" not in memory or not isinstance(memory["reminders"], dict):
        memory["reminders"] = {}
    if date not in memory["reminders"]:
        memory["reminders"][date] = []
    memory["reminders"][date].append(task)
    save_memory(memory)

def get_reminders_for_date(date):
    memory = load_memory()
    return memory.get("reminders", {}).get(date, [])
