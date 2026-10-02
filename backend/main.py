from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from routers import barang

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(barang.router, prefix="/api/barang", tags=["Barang"])

@app.on_event("startup")
def startup_event():
    database.load_data()