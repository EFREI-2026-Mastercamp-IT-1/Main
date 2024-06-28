from typing import List, Tuple ,Dict
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from src.kruskal import Graph
from src.dijkstra import GraphDijkstra
from datetime import datetime, timedelta
import pickle



app: FastAPI = FastAPI()

class Stop(BaseModel):
    """
    Class representing a stop.
    """
    stop_id: str
    stop_sequence: int
    lon: float
    lat: float
    stop_name: str

class DijkstraResponse(BaseModel):
    distance: float
    path: List[int]
    
    
class DijkstraV2Response(BaseModel):
    total_time: int
    path: List[dict]
    arrival_time: str

def get_db_connection():
    conn = sqlite3.connect('src/mon_database.db')
    conn.row_factory = sqlite3.Row
    return conn

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:4000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le graphe précalculé
with open('src/precalculated_graph.pkl', 'rb') as f:
    precalculated_graph = pickle.load(f)

@app.get("/stops/{line_name}", response_model=List[Stop])
def read_stops(line_name: str) -> List[Stop]:
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {line_name} ORDER BY stop_sequence")
    stops: List[dict] = cursor.fetchall()
    return [Stop(**dict(stop)) for stop in stops]

@app.get("/stop/{line_name}/{stop_id}", response_model=Stop)
def read_stop(line_name: str, stop_id: str) -> Stop:
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {line_name} WHERE stop_id = ?", (stop_id,)
        )
    stop: dict = cursor.fetchone()
    if stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return Stop(**dict(stop))


@app.get("/acpm")
def get_kruskal() -> List[tuple[str, str]]:
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute("SELECT * FROM new_table")
    nb_vertices: List[int] = cursor.fetchall()
    nb_vertices: List[int] = len(nb_vertices)
    g: Graph = Graph(nb_vertices)

    cursor.execute("SELECT * FROM concatligne")
    liaisons: List[List[str]] = [list(row) for row in cursor.fetchall()]

    for u, v, w in liaisons:
        g.add_edge(int(u), int(v), int(w))

    acpm: List[tuple[int, int]] = g.kruskal()

    cursor.execute("SELECT stop_ids,id FROM new_table")
    stop_ids: List[Tuple[str, int]] = cursor.fetchall()
    stop_ids: Dict[int, str] = {id: stop_id.split(',')[0] for stop_id, id in stop_ids}

    acpm_id: List[tuple[str, str]] = [(stop_ids[u], stop_ids[v]) for u, v in acpm]

    return acpm_id


@app.get("/acpm/points")
def get_kruskal_points() -> List[Stop]:
    kruskal: List[Tuple[str, str]] = get_kruskal()

    points: List[str] = []

    for u, v in kruskal:
        if u not in points:
            points.append(u)
        if v not in points:
            points.append(v)


    lines: List[str] = [
        "ligne1",
        "ligne2","ligne3","ligne3b", "ligne4", "ligne5", "ligne6", 
        "ligne7", "ligne7b", "ligne8", "ligne9", "ligne10", 
        "ligne11", "ligne12", "ligne13", "ligne14"
        ]

    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()

    stops: List[Stop] = []

    for line in lines:
        cursor.execute(f"SELECT * FROM {line}")
        stops += cursor.fetchall()

    stops: List[Stop] = [Stop(**dict(stop)) for stop in stops]

    points: List[Stop] = [stop for stop in stops if stop.stop_id in points]

    return points


@app.get("/stations/")
def read_stations() -> List[Dict[str, str]]:
    """
    I don't know what this function does
    """
    lines = [
        "ligne1","ligne2","ligne3","ligne3b", "ligne4", "ligne5", 
        "ligne6", "ligne7", "ligne7b", "ligne8", "ligne9", 
        "ligne10", "ligne11", "ligne12", "ligne13", "ligne14"
        ]
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    stations: List[Dict[str, str]] = []
    for line in lines:
        cursor.execute(
        f"""
            SELECT nt.*, l.lon, l.lat, l.stop_sequence, l.stop_id as line_stop_id
            FROM new_table nt
            JOIN {line} l ON nt.stop_ids LIKE '%' || l.stop_id || '%'
            ORDER BY l.stop_sequence
        """
        )
        line_stations: List[Dict[str, str]] = cursor.fetchall()
        for i, station in enumerate(line_stations):
            station_dict: dict = dict(station)
            station_dict["line"]: str = line
            # Add the stop_id of the next station
            if i < len(line_stations) - 1:
                next_station_id: str = line_stations[i + 1]["line_stop_id"]
                cursor.execute(
                f"""
                    SELECT id
                    FROM new_table
                    WHERE stop_ids LIKE '%' || ? || '%'
                """, (next_station_id,)
                )
                next_station_new_table_id: Dict[str, int] = cursor.fetchone()
                station_dict["next_stop_id"]: str = next_station_new_table_id["id"] if next_station_new_table_id else ""
            else:
                station_dict["next_stop_id"]: str = ""
            # Add the stop_id of the previous station
            if i > 0:
                prev_station_id: str = line_stations[i - 1]["line_stop_id"]
                cursor.execute(
                f"""
                    SELECT id
                    FROM new_table
                    WHERE stop_ids LIKE '%' || ? || '%'
                """, (prev_station_id,)
                )
                prev_station_new_table_id: Dict[str, int] = cursor.fetchone()
                station_dict["prev_stop_id"]: str = prev_station_new_table_id["id"] if prev_station_new_table_id else ""
            else:
                station_dict["prev_stop_id"]: str = ""
            stations.append(station_dict)
    return stations


@app.get("/dijkstraV2/{src_stop_id}/{dest_stop_id}/{start_time}", response_model=DijkstraV2Response)
def get_dijkstraV2(src_stop_id: str, dest_stop_id: str, start_time: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si les arrêts existent et sont des arrêts de métro
    cursor.execute("""
        SELECT s.stop_id, s.stop_name
        FROM stops s
        JOIN stop_times st ON s.stop_id = st.stop_id
        JOIN trips t ON st.trip_id = t.trip_id
        JOIN routes r ON t.route_id = r.route_id
        WHERE s.stop_id IN (?, ?) AND r.route_type = 1
        GROUP BY s.stop_id
    """, (src_stop_id, dest_stop_id))
    stops = {row['stop_id']: row['stop_name'] for row in cursor.fetchall()}
    
    if len(stops) != 2:
        raise HTTPException(status_code=400, detail="Invalid source or destination stop, or not a metro stop")

    # Utiliser le graphe précalculé
    g = precalculated_graph

    # Calculer le chemin le plus court
    start_time = datetime.strptime(start_time,  "%H:%M:%S")
    total_time, path, arrival_time = g.shortest_path(src_stop_id, dest_stop_id, start_time)

    if total_time == float('inf'):
        raise HTTPException(status_code=404, detail="No path found")

    # Construire la réponse
    trip_details = []
    for i in range(len(path) - 1):
        cursor.execute("""
            SELECT stop_name, routes.route_id, route_long_name, trip_headsign
            FROM stops 
            JOIN stop_times ON stops.stop_id = stop_times.stop_id
            JOIN trips ON stop_times.trip_id = trips.trip_id
            JOIN routes ON trips.route_id = routes.route_id
            WHERE stops.stop_id = ? AND routes.route_type = 1
            LIMIT 1
        """, (path[i],))
        stop_info = cursor.fetchone()
        trip_details.append({
            "stop_name": stop_info['stop_name'],
            "stop_id": path[i],
            "route_id": stop_info['route_id'],
            "route_name": stop_info['route_long_name'],
            "trip_headsign": stop_info['trip_headsign']
        })
    return DijkstraV2Response(
        total_time=int(total_time),
        path=trip_details,
        arrival_time=arrival_time.strftime("%Y-%m-%d %H:%M:%S")
    )
