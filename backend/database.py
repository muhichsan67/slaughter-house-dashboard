import json
import os

inventory_db = []

def load_data():
    global inventory_db
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            inventory_db = json.load(f)