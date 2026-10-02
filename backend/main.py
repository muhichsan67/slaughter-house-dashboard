from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model Data
class Barang(BaseModel):
    id: int = None
    nama: str
    kategori: str
    jumlah_stok: int
    lokasi_gudang: str

inventory_db = []

@app.on_event("startup")
def load_data():
    global inventory_db
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            inventory_db = json.load(f)