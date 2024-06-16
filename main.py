from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

class Stop(BaseModel):
    stop_id: str
    stop_sequence: int
    lon: float
    lat: float

def get_db_connection():
    conn = sqlite3.connect('mon_database.db')
    conn.row_factory = sqlite3.Row
    return conn

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:63342"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stops", response_model=List[Stop])
def read_stops():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ligne5 ORDER BY stop_sequence")
    stops = cursor.fetchall()
    return [Stop(**dict(stop)) for stop in stops]

@app.get("/stop/{stop_id}", response_model=Stop)
def read_stop(stop_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ligne5 WHERE stop_id = ?", (stop_id,))
    stop = cursor.fetchone()
    if stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return Stop(**dict(stop))
