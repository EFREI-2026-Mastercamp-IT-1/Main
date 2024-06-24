from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from starlette.middleware.cors import CORSMiddleware
from kruskal import Graph

app = FastAPI()

class Stop(BaseModel):
    stop_id: str
    stop_sequence: int
    lon: float
    lat: float
    stop_name: str

def get_db_connection():
    conn = sqlite3.connect('mon_database.db')
    conn.row_factory = sqlite3.Row
    return conn

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:4000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stops/{line_name}", response_model=List[Stop])
def read_stops(line_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {line_name} ORDER BY stop_sequence")
    stops = cursor.fetchall()
    return [Stop(**dict(stop)) for stop in stops]

@app.get("/stop/{line_name}/{stop_id}", response_model=Stop)
def read_stop(line_name: str, stop_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {line_name} WHERE stop_id = ?", (stop_id,))
    stop = cursor.fetchone()
    if stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return Stop(**dict(stop))


@app.get("/acpm")
def get_kruskal():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM new_table")
    nb_vertices = cursor.fetchall()
    nb_vertices = len(nb_vertices)
    g = Graph(nb_vertices)
    
    cursor.execute("SELECT * FROM concatligne")
    liaisons = [list(row) for row in cursor.fetchall()]
            
    for u, v, w in liaisons:
        g.add_edge(int(u), int(v), int(w))

    acpm = g.kruskal()
    
    cursor.execute("SELECT stop_ids,id FROM new_table")
    stop_ids = cursor.fetchall()
    stop_ids = {id: stop_id.split(',')[0] for stop_id, id in stop_ids}
        
    acpm_id = [(stop_ids[u], stop_ids[v]) for u, v in acpm]
    
    return acpm_id


@app.get("/acpm/points")
def get_kruskal_points():
    kruskal = get_kruskal()
    
    points = []
    
    for u, v in kruskal:
        if u not in points:
            points.append(u)
        if v not in points:
            points.append(v)
            
    
    lines = ["ligne1","ligne2","ligne3","ligne3b", "ligne4", "ligne5", "ligne6", "ligne7", "ligne7b", "ligne8", "ligne9", "ligne10", "ligne11", "ligne12", "ligne13", "ligne14"]

    conn = get_db_connection()
    cursor = conn.cursor()
    
    stops = []
    
    for line in lines:
        cursor.execute(f"SELECT * FROM {line}")
        stops += cursor.fetchall()
        
    stops = [Stop(**dict(stop)) for stop in stops]
    
    points = [stop for stop in stops if stop.stop_id in points]
    
    return points
