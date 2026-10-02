import json
import os

inventory_db = []
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    global inventory_db
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            inventory_db = json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(inventory_db, f, indent=2, ensure_ascii=False)