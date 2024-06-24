from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from starlette.middleware.cors import CORSMiddleware
import dijkstra

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
        "http://localhost:63342",
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

@app.get("/dijkstra/{start_stop}/{end_stop}")
def run_dijkstra(start_stop: str, end_stop: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les arrêts et créer un mapping de stop_id à index
    cursor.execute("SELECT stop_id FROM new_table")
    stops = cursor.fetchall()
    stop_ids = [stop['stop_id'] for stop in stops]
    stop_index = {stop_id: index for index, stop_id in enumerate(stop_ids)}

    # Initialiser les matrices d'adjacence et de coûts
    n = len(stop_ids)
    matrice_adjacence = [[0] * n for _ in range(n)]
    matrice_couts = [[float('inf')] * n for _ in range(n)]

    # Récupérer les liaisons et remplir les matrices
    cursor.execute("SELECT * FROM concatligne")
    liaisons = cursor.fetchall()
    for liaison in liaisons:
        u, v, w = stop_index[liaison['u']], stop_index[liaison['v']], liaison['w']
        matrice_adjacence[u][v] = 1
        matrice_adjacence[v][u] = 1  # Si le graphe est non orienté
        matrice_couts[u][v] = w
        matrice_couts[v][u] = w  # Si le graphe est non orienté

    # Convertir les arrêts de départ et d'arrivée en index
    start_index = stop_index.get(start_stop)
    end_index = stop_index.get(end_stop)

    if start_index is None or end_index is None:
        raise HTTPException(status_code=404, detail="Stop not found")

    # Exécuter l'algorithme de Dijkstra
    path = dijkstra(matrice_adjacence, matrice_couts, start_index, end_index)
    
    # Convertir les index du chemin en stop_ids
    path_stop_ids = [stop_ids[i] for i in path]

    return path_stop_ids


