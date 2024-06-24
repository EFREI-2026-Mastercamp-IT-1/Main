from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from starlette.middleware.cors import CORSMiddleware
from dijkstra import GraphDijkstra

app = FastAPI()

class Stop(BaseModel):
    stop_id: str
    stop_sequence: int
    lon: float
    lat: float
    stop_name: str

class DijkstraResponse(BaseModel):
    distance: float
    path: List[int]


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

@app.get("/dijkstra/{src}/{dest}", response_model=DijkstraResponse)
def get_dijkstra(src: int, dest: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM new_table")
    nb_vertices = cursor.fetchone()[0]

    g = GraphDijkstra(nb_vertices)

    cursor.execute("SELECT * FROM concatligne")
    liaisons = [list(row) for row in cursor.fetchall()]

    for u, v, w in liaisons:
        g.graph[int(u)][int(v)] = int(w)
        g.graph[int(v)][int(u)] = int(w)  # Assuming undirected graph

    if src >= nb_vertices or src < 0 or dest >= nb_vertices or dest < 0:
        raise HTTPException(status_code=400, detail="Invalid source or destination vertex")

    distance, path = g.shortest_path(src, dest)
    
    return DijkstraResponse(distance=distance, path=path)


@app.get("/stations/")
def read_stations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM new_table")
    stations = cursor.fetchall()
    return stations