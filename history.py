import json
import os

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")


def load_previous_total():
    if not os.path.exists(HISTORY_FILE):
        return None
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("total")


def save_total(total):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"total": total}, f, indent=2)