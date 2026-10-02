import json
import os

# In-memory list untuk menyimpan data
inventory_db = []

def load_data():
    global inventory_db
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            inventory_db = json.load(f)